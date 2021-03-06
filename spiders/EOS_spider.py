ف����z��'��-��&X��Ö)Z���GV>�Xqֶt���`�p�{y\�� �w�f�]�<�Uz}�;��\�'Ɨ6�2C�2s0�Kz+�)п�� �?����Y��N8
_���|�nKbDI�0{�~(AQ�X���d�e����)?jБE��ΐ��H��l.��xA;w$�s�J�`�"�՞4���ђ@�G&
:�7.��#P���������#��,l��m�R��l�6)4��[d�i�h yR���������.* ��٩�'�UR��na(;�2�<��$��-���'լw[�I�S���f���8�����Ѿ\F;>.���7@���N�7ش۳�짚���x'jI��h؇�f�Z�hvט�w�cO["��Bk�%W�P#+�z( ̙͓����M?w�~�ڭ8�7���?�T������0[��<-�LN"��s�� q��)RlE�iU�k˕/��{���g���*˅PJ�>P�n7�vN��t��ŵA��%��v�rj�ͬC	�@OX(��iC�c}��K��]�!�J��i����ˎU+�� �1��?��^S��>槸�rce6�^� �"#_ :�k�Ǎ����M��2p�AE\l��=<Q�pa&m�dq6ڋ����V6� 3PX�d�<���R��  ��A�.��ɔ��ϲ�ٷ�n�ֱ�'F��S Q��xN�^�OI���K��S����	��F��CI'��c*���N����QD`��«NM������ �Y�7
��������%�����1�jg��]��m�
���"bc;Zxn/�r$_?P;�$��̵��r���l^�-�4���ʥ+��y�A�
��4.G�x\db��4� y�K�`��r��!4��??�ɰ$^��RB��I��n�c��C�XF�-��G��c��?�j�Kx��,U�.���:"��d���<��'����dsr#@wG�eO"׊!�������K�(L�n��9˹m�O#��Id;_m9I�O�H�r�fgT,w�8��b3=[�`n(O���4��
Y2���F3��\������Dк�B�!0�����l���t}�>���]BQF�BZ�P�TH�LdGE�kBF1�q}�*��S�{[�U��y�i���Uĳ�l���^C�5�cG����HEq[���;|��,y�ܗG�� [h �����*j�b���l�`qM��t�	7��dhi:e^�2��P�)f|'��4q����HT`|r��CNd��V����
��`� &$�P�\[��_-w�T�eN��� E�S�X�O`7?�H��]D\�����~֝ =0� �b�dbT��ģ�1nj����}�ĎM�/�V̖T	<��t\'���_��d�t��7T��I�����[��n�/����1L����|��en#�m�b�b�L	�z��|���L�����aZ��)�F�5x=$[
[���0za�m4
�/n�PJ���9�>�i���9ܫD�6���,�u�8�w�����Vm�i���
        else:
            data = eval(data)
            data = data["data"]["token_details_list"]
            for item in data:
                token = {
                    "symbol": item["symbol"],
                    "account": item["exec_account"],
                    "total": item["total"],
                    "to_usd": get_currency(item),
                    "to_btc": get_currency(item)/be_cur["BTC"],
                    "to_eth": get_currency(item)/be_cur["ETH"]
                }
                res.append(token)
    return res


def get_currency(item):
    #汇率使用总市值和发行量计算得到，汇率最终保留到6位小数
    supply = float(item["supply"])
    total = float(item["total"])
    if supply == 0:
        return 0
    else:
        return round(total/supply,6)


def job(url,be_cur):
    #主要请求函数，最后会返回货币信息列表
    try:
        web_data = requests.get(url,timeout = (1,4)) #网速好0.3秒完成一个页面，这里的连接超时阈值设置为1秒，读取超时4秒
        logger.info(web_data)
        soup = BeautifulSoup(web_data.text, "lxml")
        data = process_raw_data(soup.get_text(),be_cur)
        for i in data:
            i["time"] = process_time(datetime.now())
        return data
    except RuntimeError:
        logger.error("RunTimeError",exc_info = True)
        print("RuntimeError")
        pass
    except requests.exceptions.ConnectTimeout:
        logger.error("Time Out",exc_info = True)
        print("Time out")
        pass
    except socket.timeout:
        logger.error("Web Socket Timeout")
        print("Web Socket Timeout")
        pass
    except urllib3.exceptions.ReadTimeoutError:
        logger.error("Read Time Out")
        print("Web Read Time Out")
        pass
    except requests.exceptions.ReadTimeout:
        logger.error("Read Time Out")
        print("Web Read Time Out")
        pass
    except OpenSSL.SSL.WantReadError:
        logger.error("Want Read Error")
        print("Want Read Error")
        pass
    except requests.exceptions.ConnectionError:
        logger.error("Web Connection Error")
        print("Connection Error")
        pass
    except:
        logger.error("Some Error Happened",exc_info = True)
        pass


def main():
    #主函数，会打印抓取结果，打印抓取时间，返回包含所有货币信息的列表
    be_cur = btc_eth.main()
    res = []
    for url in config.EOS_configs["urls"]:
        try:
            res.extend(job(url,be_cur))
        except:
            pass
        continue
    return res



if __name__ == "__main__":
    print(main()) #最大值为203

be_cur = {"BTC":10,"ETH":5}
@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_process_raw_data(index):
    url = "https://eospark.com/api/v2/tokens?token_name=&page=5&size=20&sort_field=total&sort_order=descend"
    assert process_raw_data("",be_cur) == []
    assert type(job(url,be_cur)) == type([])
    assert len(job(url,be_cur)) > 5
    assert type(job(url,be_cur)[index]) == type({})
    assert len(job(url,be_cur)[index]) == 7

@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_main_return(index):
    assert type(main()) == type([])
    assert len(main()) >5
    assert type(main()[index]) == type({})
    assert len(main()[index]) == 7



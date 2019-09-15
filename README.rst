===============
ctpbee_analyzer
===============

---------------
示例
---------------

::

    from ctpbee_analyzer import cost
    @cost
    def test1():
        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        del b
        return a


    @cost
    def test2():
        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        return a


    if __name__ == '__main__':
        test1()
        test2()



::

 >>
    Function        Spend           CPU             Memory
    ===============================================================
    test1           111.734 ms      98.4 %          19.164 MiB

    Function        Spend           CPU             Memory
    ===============================================================
    test2           110.564 ms      108.5 %         171.629 MiB
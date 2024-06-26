from omint.OMCConnection import OMCConnection


def test__start_omc_process():
    omc = OMCConnection()
    proc = omc._start_omc_process(False, 10000)

    assert proc.pid

    proc.terminate()

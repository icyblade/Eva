def test_init():
    from eva.pms import PMS

    pms = PMS()

    pms.budget = {'budget': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}
    assert pms.budget == {'budget': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}

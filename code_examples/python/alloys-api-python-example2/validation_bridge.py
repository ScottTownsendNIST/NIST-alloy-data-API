import ValidationLibrary as VL

def validation_bridge(val, var, in_unit, rep):
    tuple0 = ("", "", "", f"{val}", "", var, in_unit)
    if (var[0] == 'H' or var[0] == 'G') and rep == 'A':
        check_val = ['bool','False', 0.0,'Direct Representation of Relational Value',var.lower()]
        err_mess = 'Direct Representation of Relational Value'
    elif var == 'VDN':
        check_val = VL.Validate_VDN(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VDC':
        check_val = VL.Validate_VDC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VS':
        check_val = VL.Validate_VS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VSC':
        check_val = VL.Validate_VSC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VM':
        check_val = VL.Validate_VM(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VEX':
        check_val = VL.Validate_VEX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VC':
        check_val = VL.Validate_VC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VA':
        check_val = VL.Validate_VA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VDM':
        check_val = VL.Validate_VDM(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'P':
        check_val = VL.Validate_P(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PP':
        check_val = VL.Validate_PP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PC':
        check_val = VL.Validate_PC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PUC':
        check_val = VL.Validate_PUC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PX':
        check_val = VL.Validate_PX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PL':
        check_val = VL.Validate_PL(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PU':
        check_val = VL.Validate_PU(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PV':
        check_val = VL.Validate_PV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TPP':
        check_val = VL.Validate_TPP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'RSS':
        check_val = VL.Validate_RSS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'IST':
        check_val = VL.Validate_IST(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'IIT':
        check_val = VL.Validate_IIT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NVK':
        check_val = VL.Validate_NVK(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NVC':
        check_val = VL.Validate_NVC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'T':
        check_val = VL.Validate_T(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TL':
        check_val = VL.Validate_TL(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TU':
        check_val = VL.Validate_TU(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TB':
        check_val = VL.Validate_TB(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TC':
        check_val = VL.Validate_TC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TE':
        check_val = VL.Validate_TE(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TM':
        check_val = VL.Validate_TM(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TBN':
        check_val = VL.Validate_TBN(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TMN':
        check_val = VL.Validate_TMN(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TT':
        check_val = VL.Validate_TT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TPT':
        check_val = VL.Validate_TPT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TR':
        check_val = VL.Validate_TR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TX':
        check_val = VL.Validate_TX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TUC':
        check_val = VL.Validate_TUC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NTC':
        check_val = VL.Validate_NTC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NTD':
        check_val = VL.Validate_NTD(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NDC':
        check_val = VL.Validate_NDC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CP':
        check_val = VL.Validate_CP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CPW':
        check_val = VL.Validate_CPW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CPV':
        check_val = VL.Validate_CPV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CPA':
        check_val = VL.Validate_CPA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CEX':
        check_val = VL.Validate_CEX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CPEH':
        check_val = VL.Validate_CPEHW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CPEHW':
        check_val = VL.Validate_CPEHW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CV':
        check_val = VL.Validate_CV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CVW':
        check_val = VL.Validate_CVW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CVV':
        check_val = VL.Validate_CVV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CS':
        check_val = VL.Validate_CS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'CGM':
        check_val = VL.Validate_CGM(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HW':
        check_val = VL.Validate_HW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'H':
        check_val = VL.Validate_H(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HTR':
        check_val = VL.Validate_HTR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HSL':
        check_val = VL.Validate_HSL(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HRX':
        check_val = VL.Validate_HRX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HTRW':
        check_val = VL.Validate_HTRW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HVP':
        check_val = VL.Validate_HVP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HA':
        check_val = VL.Validate_HA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HEX':
        check_val = VL.Validate_HEX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HEXW':
        check_val = VL.Validate_HEXW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HP':
        check_val = VL.Validate_HP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HXM':
        check_val = VL.Validate_HXM(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HX':
        check_val = VL.Validate_HX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'G':
        check_val = VL.Validate_G(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GP':
        check_val = VL.Validate_GP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GR':
        check_val = VL.Validate_GR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GA':
        check_val = VL.Validate_GA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GEX':
        check_val = VL.Validate_GEX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'UA':
        check_val = VL.Validate_UA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'U':
        check_val = VL.Validate_U(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'UV':
        check_val = VL.Validate_UV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LE':
        check_val = VL.Validate_LE(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'S':
        check_val = VL.Validate_S(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'SA':
        check_val = VL.Validate_SA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'SEX':
        check_val = VL.Validate_SEX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'SR':
        check_val = VL.Validate_SR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'SP':
        check_val = VL.Validate_SP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'SW':
        check_val = VL.Validate_SW(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LA':
        check_val = VL.Validate_LA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LB':
        check_val = VL.Validate_LB(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LC':
        check_val = VL.Validate_LC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LAA':
        check_val = VL.Validate_LAA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LAB':
        check_val = VL.Validate_LAB(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LAC':
        check_val = VL.Validate_LAC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'RLE':
        check_val = VL.Validate_RLE(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'RVE':
        check_val = VL.Validate_RVE(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LEC':
        check_val = VL.Validate_LEC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VTP':
        check_val = VL.Validate_VTP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VPT':
        check_val = VL.Validate_VPT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'EH':
        check_val = VL.Validate_EH(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'ENT':
        check_val = VL.Validate_ENT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'EN':
        check_val = VL.Validate_EN(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'EHS':
        check_val = VL.Validate_EHS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'AP':
        check_val = VL.Validate_AP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'AC':
        check_val = VL.Validate_AC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GRV':
        check_val = VL.Validate_GRV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'WB':
        check_val = VL.Validate_WB(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'WH':
        check_val = VL.Validate_WH(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MMS':
        check_val = VL.Validate_MMS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MSS':
        check_val = VL.Validate_MSS(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MP':
        check_val = VL.Validate_MP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MPR':
        check_val = VL.Validate_MPR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'ER':
        check_val = VL.Validate_ER(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'ERX':
        check_val = VL.Validate_ERX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'EC':
        check_val = VL.Validate_EC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'WL':
        check_val = VL.Validate_WL(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MAS':
        check_val = VL.Validate_mas(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'ATM':
        check_val = VL.Validate_atm(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'MOL':
        check_val = VL.Validate_mol(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'W':
        check_val = VL.Validate_W(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'X':
        check_val = VL.Validate_X(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VOP':
        check_val = VL.Validate_VOP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NOP':
        check_val = VL.Validate_NOP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'STE':
        check_val = VL.Validate_ste(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HRT':
        check_val = VL.Validate_hrt(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'Z':
        check_val = VL.Validate_Z(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'ZC':
        check_val = VL.Validate_ZC(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VPA':
        check_val = VL.Validate_VPA(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HT':
        check_val = VL.Validate_HT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'KJ':
        check_val = VL.Validate_KJ(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'KX':
        check_val = VL.Validate_KX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'KP':
        check_val = VL.Validate_KP(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'VVE':
        check_val = VL.Validate_VVE(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'NFL':
        check_val = VL.Validate_NFL(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'WF':
        check_val = VL.Validate_WF(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'GT':
        check_val = VL.Validate_GT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'TJT':
        check_val = VL.Validate_TJT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'LAR':
        check_val = VL.Validate_LAR(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HPT':
        check_val = VL.Validate_HPT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'RIX':
        check_val = VL.Validate_RIX(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PTV':
        check_val = VL.Validate_PTV(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'KT':
        check_val = VL.Validate_KT(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'HRTS':
        check_val = VL.Validate_hrts(tuple0)
        err_mess = 'Value Out of Valid Range'
    elif var == 'PRTS':
        check_val = VL.Validate_prts(tuple0)
        err_mess = 'Value Out of Valid Range'
    
    return(check_val, err_mess)
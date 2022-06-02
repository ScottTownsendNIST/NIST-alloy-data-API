import ValidationLibrary as VL

def validation_bridge(val, var, in_unit, rep):
    tuple0 = ("", "", "", f"{val}", "", var, in_unit)
    if (var[0] == 'H' or var[0] == 'G') and rep == 'A':
        check_val = ['bool','False', 0.0,'Direct Representation of Relational Value',var.lower()]
    elif var == 'VDN':
        check_val = VL.Validate_VDN(tuple0)
    elif var == 'VDC':
        check_val = VL.Validate_VDC(tuple0)
    elif var == 'VS':
        check_val = VL.Validate_VS(tuple0)
    elif var == 'VSC':
        check_val = VL.Validate_VSC(tuple0)
    elif var == 'VM':
        check_val = VL.Validate_VM(tuple0)
    elif var == 'VEX':
        check_val = VL.Validate_VEX(tuple0)
    elif var == 'VC':
        check_val = VL.Validate_VC(tuple0)
    elif var == 'VA':
        check_val = VL.Validate_VA(tuple0)
    elif var == 'VDM':
        check_val = VL.Validate_VDM(tuple0)
    elif var == 'P':
        check_val = VL.Validate_P(tuple0)
    elif var == 'PP':
        check_val = VL.Validate_PP(tuple0)
    elif var == 'PC':
        check_val = VL.Validate_PC(tuple0)
    elif var == 'PUC':
        check_val = VL.Validate_PUC(tuple0)
    elif var == 'PX':
        check_val = VL.Validate_PX(tuple0)
    elif var == 'PL':
        check_val = VL.Validate_PL(tuple0)
    elif var == 'PU':
        check_val = VL.Validate_PU(tuple0)
    elif var == 'PV':
        check_val = VL.Validate_PV(tuple0)
    elif var == 'TPP':
        check_val = VL.Validate_TPP(tuple0)
    elif var == 'RSS':
        check_val = VL.Validate_RSS(tuple0)
    elif var == 'IST':
        check_val = VL.Validate_IST(tuple0)
    elif var == 'IIT':
        check_val = VL.Validate_IIT(tuple0)
    elif var == 'NVK':
        check_val = VL.Validate_NVK(tuple0)
    elif var == 'NVC':
        check_val = VL.Validate_NVC(tuple0)
    elif var == 'T':
        check_val = VL.Validate_T(tuple0)
    elif var == 'TL':
        check_val = VL.Validate_TL(tuple0)
    elif var == 'TU':
        check_val = VL.Validate_TU(tuple0)
    elif var == 'TB':
        check_val = VL.Validate_TB(tuple0)
    elif var == 'TC':
        check_val = VL.Validate_TC(tuple0)
    elif var == 'TE':
        check_val = VL.Validate_TE(tuple0)
    elif var == 'TM':
        check_val = VL.Validate_TM(tuple0)
    elif var == 'TBN':
        check_val = VL.Validate_TBN(tuple0)
    elif var == 'TMN':
        check_val = VL.Validate_TMN(tuple0)
    elif var == 'TT':
        check_val = VL.Validate_TT(tuple0)
    elif var == 'TPT':
        check_val = VL.Validate_TPT(tuple0)
    elif var == 'TR':
        check_val = VL.Validate_TR(tuple0)
    elif var == 'TX':
        check_val = VL.Validate_TX(tuple0)
    elif var == 'TUC':
        check_val = VL.Validate_TUC(tuple0)
    elif var == 'NTC':
        check_val = VL.Validate_NTC(tuple0)
    elif var == 'NTD':
        check_val = VL.Validate_NTD(tuple0)
    elif var == 'NDC':
        check_val = VL.Validate_NDC(tuple0)
    elif var == 'CP':
        check_val = VL.Validate_CP(tuple0)
    elif var == 'CPW':
        check_val = VL.Validate_CPW(tuple0)
    elif var == 'CPV':
        check_val = VL.Validate_CPV(tuple0)
    elif var == 'CPA':
        check_val = VL.Validate_CPA(tuple0)
    elif var == 'CEX':
        check_val = VL.Validate_CEX(tuple0)
    elif var == 'CPEH':
        check_val = VL.Validate_CPEHW(tuple0)
    elif var == 'CPEHW':
        check_val = VL.Validate_CPEHW(tuple0)
    elif var == 'CV':
        check_val = VL.Validate_CV(tuple0)
    elif var == 'CVW':
        check_val = VL.Validate_CVW(tuple0)
    elif var == 'CVV':
        check_val = VL.Validate_CVV(tuple0)
    elif var == 'CS':
        check_val = VL.Validate_CS(tuple0)
    elif var == 'CGM':
        check_val = VL.Validate_CGM(tuple0)
    elif var == 'HW':
        check_val = VL.Validate_HW(tuple0)
    elif var == 'H':
        check_val = VL.Validate_H(tuple0)
    elif var == 'HTR':
        check_val = VL.Validate_HTR(tuple0)
    elif var == 'HSL':
        check_val = VL.Validate_HSL(tuple0)
    elif var == 'HRX':
        check_val = VL.Validate_HRX(tuple0)
    elif var == 'HTRW':
        check_val = VL.Validate_HTRW(tuple0)
    elif var == 'HVP':
        check_val = VL.Validate_HVP(tuple0)
    elif var == 'HA':
        check_val = VL.Validate_HA(tuple0)
    elif var == 'HEX':
        check_val = VL.Validate_HEX(tuple0)
    elif var == 'HEXW':
        check_val = VL.Validate_HEXW(tuple0)
    elif var == 'HP':
        check_val = VL.Validate_HP(tuple0)
    elif var == 'HXM':
        check_val = VL.Validate_HXM(tuple0)
    elif var == 'HX':
        check_val = VL.Validate_HX(tuple0)
    elif var == 'G':
        check_val = VL.Validate_G(tuple0)
    elif var == 'GP':
        check_val = VL.Validate_GP(tuple0)
    elif var == 'GR':
        check_val = VL.Validate_GR(tuple0)
    elif var == 'GA':
        check_val = VL.Validate_GA(tuple0)
    elif var == 'GEX':
        check_val = VL.Validate_GEX(tuple0)
    elif var == 'UA':
        check_val = VL.Validate_UA(tuple0)
    elif var == 'U':
        check_val = VL.Validate_U(tuple0)
    elif var == 'UV':
        check_val = VL.Validate_UV(tuple0)
    elif var == 'LE':
        check_val = VL.Validate_LE(tuple0)
    elif var == 'S':
        check_val = VL.Validate_S(tuple0)
    elif var == 'SA':
        check_val = VL.Validate_SA(tuple0)
    elif var == 'SEX':
        check_val = VL.Validate_SEX(tuple0)
    elif var == 'SR':
        check_val = VL.Validate_SR(tuple0)
    elif var == 'SP':
        check_val = VL.Validate_SP(tuple0)
    elif var == 'SW':
        check_val = VL.Validate_SW(tuple0)
    elif var == 'LA':
        check_val = VL.Validate_LA(tuple0)
    elif var == 'LB':
        check_val = VL.Validate_LB(tuple0)
    elif var == 'LC':
        check_val = VL.Validate_LC(tuple0)
    elif var == 'LAA':
        check_val = VL.Validate_LAA(tuple0)
    elif var == 'LAB':
        check_val = VL.Validate_LAB(tuple0)
    elif var == 'LAC':
        check_val = VL.Validate_LAC(tuple0)
    elif var == 'RLE':
        check_val = VL.Validate_RLE(tuple0)
    elif var == 'RVE':
        check_val = VL.Validate_RVE(tuple0)
    elif var == 'LEC':
        check_val = VL.Validate_LEC(tuple0)
    elif var == 'VTP':
        check_val = VL.Validate_VTP(tuple0)
    elif var == 'VPT':
        check_val = VL.Validate_VPT(tuple0)
    elif var == 'EH':
        check_val = VL.Validate_EH(tuple0)
    elif var == 'ENT':
        check_val = VL.Validate_ENT(tuple0)
    elif var == 'EN':
        check_val = VL.Validate_EN(tuple0)
    elif var == 'EHS':
        check_val = VL.Validate_EHS(tuple0)
    elif var == 'AP':
        check_val = VL.Validate_AP(tuple0)
    elif var == 'AC':
        check_val = VL.Validate_AC(tuple0)
    elif var == 'GRV':
        check_val = VL.Validate_GRV(tuple0)
    elif var == 'WB':
        check_val = VL.Validate_WB(tuple0)
    elif var == 'WH':
        check_val = VL.Validate_WH(tuple0)
    elif var == 'MMS':
        check_val = VL.Validate_MMS(tuple0)
    elif var == 'MSS':
        check_val = VL.Validate_MSS(tuple0)
    elif var == 'MP':
        check_val = VL.Validate_MP(tuple0)
    elif var == 'MPR':
        check_val = VL.Validate_MPR(tuple0)
    elif var == 'ER':
        check_val = VL.Validate_ER(tuple0)
    elif var == 'ERX':
        check_val = VL.Validate_ERX(tuple0)
    elif var == 'EC':
        check_val = VL.Validate_EC(tuple0)
    elif var == 'WL':
        check_val = VL.Validate_WL(tuple0)
    elif var == 'MAS':
        check_val = VL.Validate_mas(tuple0)
    elif var == 'ATM':
        check_val = VL.Validate_atm(tuple0)
    elif var == 'MOL':
        check_val = VL.Validate_mol(tuple0)
    elif var == 'W':
        check_val = VL.Validate_W(tuple0)
    elif var == 'X':
        check_val = VL.Validate_X(tuple0)
    elif var == 'VOP':
        check_val = VL.Validate_VOP(tuple0)
    elif var == 'NOP':
        check_val = VL.Validate_NOP(tuple0)
    elif var == 'STE':
        check_val = VL.Validate_ste(tuple0)
    elif var == 'HRT':
        check_val = VL.Validate_hrt(tuple0)
    elif var == 'Z':
        check_val = VL.Validate_Z(tuple0)
    elif var == 'ZC':
        check_val = VL.Validate_ZC(tuple0)
    elif var == 'VPA':
        check_val = VL.Validate_VPA(tuple0)
    elif var == 'HT':
        check_val = VL.Validate_HT(tuple0)
    elif var == 'KJ':
        check_val = VL.Validate_KJ(tuple0)
    elif var == 'KX':
        check_val = VL.Validate_KX(tuple0)
    elif var == 'KP':
        check_val = VL.Validate_KP(tuple0)
    elif var == 'VVE':
        check_val = VL.Validate_VVE(tuple0)
    elif var == 'NFL':
        check_val = VL.Validate_NFL(tuple0)
    elif var == 'WF':
        check_val = VL.Validate_WF(tuple0)
    elif var == 'GT':
        check_val = VL.Validate_GT(tuple0)
    elif var == 'TJT':
        check_val = VL.Validate_TJT(tuple0)
    elif var == 'LAR':
        check_val = VL.Validate_LAR(tuple0)
    elif var == 'HPT':
        check_val = VL.Validate_HPT(tuple0)
    elif var == 'RIX':
        check_val = VL.Validate_RIX(tuple0)
    elif var == 'PTV':
        check_val = VL.Validate_PTV(tuple0)
    elif var == 'KT':
        check_val = VL.Validate_KT(tuple0)
    elif var == 'HRTS':
        check_val = VL.Validate_hrts(tuple0)
    elif var == 'PRTS':
        check_val = VL.Validate_prts(tuple0)
    
    return(check_val)
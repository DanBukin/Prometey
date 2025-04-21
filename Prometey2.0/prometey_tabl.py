"""
Модуль для генерации таблиц и экспорта расчётных данных в Excel.

Основные функции:
- Формирование DataFrame из результатов расчётов,
- Запись данных в `.xlsx`,
- Создание промежуточных таблиц по этапам теплового анализа.

Модуль используется для документирования результатов и визуального контроля.
"""
from prometey_functions import *
from scipy.interpolate import griddata, RBFInterpolator, interp1d
from itertools import islice
def tabl_1(X, Y):
    print('')
    print('-----------------------------------Таблица 1-------------------------------------')
    d_kp = 2 * min(Y)
    index_d_kp = Y.index(min(Y))
    print(f'Диаметр критики равен {d_kp:.6f} м, его индекс: {index_d_kp}')
    number=[]
    D = []
    D_otn = []
    F = []
    F_otn = []
    delta_S=[]
    k=0
    for i in Y:
        number.append(k)
        D.append(2 * i)
        D_otn.append(2 * i / d_kp)
        F.append(math.pi * 2 * i * 2 * i / 4)
        F_otn.append((math.pi * 2 * i * 2 * i / 4) / (math.pi * d_kp * d_kp / 4))
        k+=1
    delta_x = np.diff(X)
    delta_x_s = np.sqrt(np.diff(X) ** 2 + np.diff(Y) ** 2)
    for i in range(0,len(Y)-1):
        delta_S.append(math.pi * 0.5 * (D[i] + D[i + 1])*delta_x_s[i])
    delta_S=np.append(delta_S, np.nan)

    # Дополняем delta_x и delta_x_s до длины X и Y
    delta_x = np.append(delta_x, np.nan)  # Добавляем NaN в конец
    delta_x_s = np.append(delta_x_s, np.nan)  # Добавляем NaN в конец

    # Создание DataFrame
    df = pd.DataFrame({
        'X': X,
        'D': D,
        'D_отн': D_otn,
        'F': F,
        'F_отн': F_otn,
        'ΔX': delta_x,
        'ΔX_s': delta_x_s,
        "ΔS":delta_S
    })

    # Замена NaN на прочерки
    df_filled = df.fillna('-')

    # Настройка отображения всех строк и столбцов
    pd.set_option('display.max_rows', None)  # Показать все строки
    df_filled.to_excel('table1.xlsx', index=False)  # Сохранить в Excel
    # Сохранение таблицы в файл (опционально)
    # Вывод таблицы
    print(df_filled)
    print('---------------------------------------------------------------------------------')
    print('')
    return number,X,D,D_otn,F,F_otn,delta_x,delta_x_s,d_kp,delta_S
def tabl_2(D,delta_st,h,n_r_array,beta_reb,delta_reb):
    print('')
    print('-----------------------------------Таблица 2-------------------------------------')
    t=[]
    D_05=[]
    t_N=[]
    f=[]
    d_g=[]
    for index,i in enumerate(D):
        D_05.append((i * ((1 + ((2 * delta_st + h)) / i))))
        t.append(math.pi*(i * ((1 + ((2 * delta_st + h)) / i)))*1000/n_r_array[index])
        t_N.append(t[index]*math.cos(beta_reb))
        f.append(t_N[index]*0.001*h*(1-(delta_reb/(t_N[index]*0.001)))*n_r_array[index])
        d_g.append((2*h*(t_N[index]*0.001-delta_reb)/(t_N[index]*0.001-delta_reb+h))*1000)
    # Создание DataFrame
    df = pd.DataFrame({
        'n_r': n_r_array,
        't, мм': t,
        't_N, мм': t_N,
        'f, м2': f,
        'd_г, мм': d_g
    })

    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table2.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
    print('---------------------------------------------------------------------------------')
    print('')
    return n_r_array,t,t_N,f,d_g
def tabl_3(q_kon,q_l,q_sum,X,betta,T_st_otn,lambd,S_1):
    print('')
    print('-----------------------------------Таблица 3-------------------------------------')
    # Создание DataFrame
    df = pd.DataFrame({
        'X, мм': X,
        'λ':lambd ,
        'β': betta,
        'S':S_1 ,
        'T_отн_ст':T_st_otn ,
        'q_к, МВт/м2': q_kon,
        'q_л, МВт/м2': q_l,
        'q_сум, МВт/м2': q_sum,
    })

    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table3.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
    print('---------------------------------------------------------------------------------')
    print('')
    return q_kon,q_l,q_sum,X,betta,T_st_otn,lambd,S_1
def tabl_4(T_ohl,C_p_raznitsa,C_p_ohl,p_ohl,f,m_ohl,d_g,delta_reb,h,beta_reb,t,lambda_st_vn,T_aray, p_aray, rho_aray, C_aray, mu_aray, lambda_aray, K_aray,name_ohl):
    print('')
    print('-----------------------------------Таблица 4-------------------------------------')
    lambda_ohl=[]
    mu_ohl=[]
    K_ohl=[]
    rho_ohl=[]
    u_ohl=[]
    alpha_ohl=[]
    k=0
    Bio=[]
    psi=[]
    E=[]
    kpd_r=[]
    t = np.array(t)
    t = t *0.001
    complex_components = {"Водород", "АТ", "Кислород", "Гелий", "Аммиак", "Метан"}

    if name_ohl in complex_components:
        # p_aray обязателен!
        points = np.column_stack((T_aray, p_aray))

        for i, p_i in zip(T_ohl, p_ohl):
            test_point = np.array([i, p_i])

            def safe_interp(arr):
                if is_inside(points, test_point):
                    val = griddata(points, arr, (i, p_i), method='cubic')
                else:
                    rbf = RBFInterpolator(points, arr, kernel='thin_plate_spline')
                    val = rbf([[i, p_i]])[0]
                return float(val)
            lambda_ohl.append(safe_interp(lambda_aray))
            mu_ohl.append(safe_interp(mu_aray))
            K_ohl.append(safe_interp(K_aray))
            rho_ohl.append(safe_interp(rho_aray))

    else:
        # Только T_aray, никаких p_aray
        def interp_1d(arr):
            f = interp1d(T_aray, arr, kind='linear', fill_value='extrapolate')
            return float(f(i))

        for i in T_ohl:
            lambda_ohl.append(interp_1d(lambda_aray))
            mu_ohl.append(interp_1d(mu_aray))
            K_ohl.append(interp_1d(K_aray))
            rho_ohl.append(interp_1d(rho_aray))
    k=0
    for i in T_ohl:
        u_ohl.append(m_ohl[k]/(f[k]*rho_ohl[k]))
        alpha_ohl.append((0.023*K_ohl[k]*((m_ohl[k]/f[k])**0.8))/((d_g[k]*0.001)**0.2))
        Bio.append(alpha_ohl[k]/(lambda_st_vn[k]/delta_reb))
        psi.append((h/delta_reb)*((2*Bio[k])**(0.5)))# МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ
        E.append(math.tanh(psi[k]) / psi[k])  # МАЗЕРАТТИ
        kpd_r.append(1 + ((1 / math.cos(beta_reb)) * (2 * (h / t[k]) * E[k] - (delta_reb / t[k]))))
        k+=1
    print("u_ohl:", len(u_ohl))
    print("T_ohl:", len(T_ohl))
    print("C_p_ohl:", len(C_p_ohl))
    print("lambda_ohl:", len(lambda_ohl))
    print("mu_ohl:", len(mu_ohl))
    print("K_ohl:", len(K_ohl))
    print("rho_ohl:", len(rho_ohl))
    print("alpha_ohl:", len(alpha_ohl))
    print("E:", len(E))
    print("kpd_r:", len(kpd_r))
    # Создание DataFrame
    df = pd.DataFrame({
        'T_охл': T_ohl,
        'ΔC,%':C_p_raznitsa ,
        'C_p_охл': C_p_ohl,
        "λ_охл":lambda_ohl,
        "μ_охл":mu_ohl,
        "K_охл":K_ohl,
        "ρ_охл":rho_ohl,
        "α_охл":alpha_ohl,
        "E": E,
        "η_р": kpd_r,
        "u_ohl":u_ohl
    })

    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table4.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
    print('---------------------------------------------------------------------------------')
    print('')
    return u_ohl,T_ohl,C_p_raznitsa ,C_p_ohl,lambda_ohl,mu_ohl,K_ohl,rho_ohl,alpha_ohl,E,kpd_r
def tabl_4_AT_NDMG(ind_peret,T_ohl,C_p_raznitsa,C_p_ohl,p_ohl,f,m_ohl,d_g,delta_reb,h,beta_reb,t,lambda_st_vn,T_aray_1, p_aray_1, rho_aray_1, C_aray_1, mu_aray_1, lambda_aray_1, K_aray_1,T_aray_2, p_aray_2, rho_aray_2, C_aray_2, mu_aray_2, lambda_aray_2, K_aray_2,name_ohl):
    print('')
    print('-----------------------------------Таблица 4-------------------------------------')
    lambda_ohl = []
    mu_ohl = []
    K_ohl = []
    rho_ohl = []
    u_ohl = []
    alpha_ohl = []
    k = 0
    Bio = []
    psi = []
    E = []
    kpd_r = []
    t = np.array(t)
    t = t * 0.001

    # Только T_aray, никаких p_aray
    def interp_1d(arr):
        f = interp1d(T_aray_2, arr, kind='linear', fill_value='extrapolate')
        return float(f(i))

    for i in T_ohl[:ind_peret]:
        lambda_ohl.append(interp_1d(lambda_aray_2))
        mu_ohl.append(interp_1d(mu_aray_2))
        K_ohl.append(interp_1d(K_aray_2))
        rho_ohl.append(interp_1d(rho_aray_2))

    # p_aray обязателен!
    points = np.column_stack((T_aray_1, p_aray_1))

    for i, p_i in zip(T_ohl[ind_peret:], p_ohl[ind_peret:]):
        test_point = np.array([i, p_i])

        def safe_interp(arr):
            if is_inside(points, test_point):
                val = griddata(points, arr, (i, p_i), method='cubic')
            else:
                rbf = RBFInterpolator(points, arr, kernel='thin_plate_spline')
                val = rbf([[i, p_i]])[0]
            return float(val)

        lambda_ohl.append(safe_interp(lambda_aray_1))
        mu_ohl.append(safe_interp(mu_aray_1))
        K_ohl.append(safe_interp(K_aray_1))
        rho_ohl.append(safe_interp(rho_aray_1))
    k = 0
    for i in T_ohl:
        u_ohl.append(m_ohl[k] / (f[k] * rho_ohl[k]))
        alpha_ohl.append((0.023 * K_ohl[k] * ((m_ohl[k] / f[k]) ** 0.8)) / ((d_g[k] * 0.001) ** 0.2))
        Bio.append(alpha_ohl[k] / (lambda_st_vn[k] / delta_reb))
        psi.append((h / delta_reb) * ((2 * Bio[k]) ** (0.5)))  # МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ# МАЗЕРАТТИ
        E.append(math.tanh(psi[k]) / psi[k])  # МАЗЕРАТТИ
        kpd_r.append(1 + ((1 / math.cos(beta_reb)) * (2 * (h / t[k]) * E[k] - (delta_reb / t[k]))))
        k += 1
    # Создание DataFrame
    df = pd.DataFrame({
        'T_охл': T_ohl,
        'ΔC,%': C_p_raznitsa,
        'C_p_охл': C_p_ohl,
        "λ_охл": lambda_ohl,
        "μ_охл": mu_ohl,
        "K_охл": K_ohl,
        "ρ_охл": rho_ohl,
        "α_охл": alpha_ohl,
        "E": E,
        "η_р": kpd_r,
        "u_ohl": u_ohl
    })
    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table4.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
    print('---------------------------------------------------------------------------------')
    print('')
    return u_ohl,T_ohl,C_p_raznitsa ,C_p_ohl,lambda_ohl,mu_ohl,K_ohl,rho_ohl,alpha_ohl,E,kpd_r
def tabl_5(c,delta_sheroh,u_ohl,rho_ohl,d_g,mu_ohl,t_N,delta_reb,h,delta_x_s,beta_reb,p_ohl,variant_ohl,ind_peret=0,p_ohl_2=0):
    p_ohl=p_ohl*1000000
    p_ohl_2 = p_ohl_2 * 1000000
    p_nach_228=p_ohl
    x = np.array([0.05,0.1,0.2,0.3,0.4,0.5,0.7,1.0])
    y = np.array([1.5,1.32,1.25,1.10,1.03,0.97,0.91,0.9])
    Re=[]
    Re_gr=[]
    delta_sheroh_otn=[]
    epsilon=[]
    omega=[]
    delta_p=[]
    delta_p_sum=0
    p_itog=[]
    l=[]
    i=0
    for rho,u,d,mu,t,x_s in zip(rho_ohl,u_ohl,d_g,mu_ohl,t_N,delta_x_s):
        Re.append(rho*u*d*0.001/mu)
        delta_sheroh_otn.append(delta_sheroh/(d*0.001))
        omega.append((np.interp(((t*0.001-delta_reb)/h), x, y, left=y[0], right=y[-1])))
        Re_gr.append(560/delta_sheroh_otn[i])
        if Re[i]<=3500:
            epsilon.append(64*omega[i]/Re[i])
        elif 3500<Re[i]<=Re_gr[i]:
            if 0.01<=delta_sheroh_otn[i]<=0.6001:
                epsilon.append(0.1*((1.46*delta_sheroh_otn[i]+(100/Re[i]))**0.25)*omega[i])
            else:
                epsilon.append((1.42*omega[i])/((math.log10(Re[i]/delta_sheroh_otn[i]))**2))
        else:
            epsilon.append(omega[i]/((2*math.log10(3.7/delta_sheroh_otn[i]))**2))
        l.append(x_s/(math.cos(beta_reb)))
        delta_p.append(c*epsilon[i]*rho*u*u*0.5*l[i]/(d*0.001))
        if i!=len(rho_ohl)-1:
            delta_p_sum+=delta_p[i]
        i += 1

    if variant_ohl==1 or variant_ohl==5:
        q=0
        p_itog.append(p_ohl)
        while q<=ind_peret:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q+=1
        p_itog_peret=p_ohl
        while q<=len(rho_ohl)-2:
            p_itog.append(p_ohl - delta_p[q])
            p_ohl = p_ohl - (delta_p[q])
            q += 1
    elif variant_ohl==3:
        q = ind_peret
        while q < len(rho_ohl)-1:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q += 1
        first=p_itog
        p_itog=[]
        q=ind_peret
        p_ohl=first[-1]
        while q>=0:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q -= 1
        second=p_itog
        p_itog=second[::-1]+first
    elif variant_ohl==4:
        q = 0
        while q <= ind_peret:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q += 1
        q = len(rho_ohl)-2
        first=p_itog
        p_itog=[]
        while q >= ind_peret:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q -= 1
        second=p_itog
        p_itog_peret = second[-1]
        p_itog = first + second[::-1]
    elif variant_ohl==6:
        q=0
        while q <= ind_peret:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q += 1
        q = ind_peret
        first=p_itog
        print(f'first={len(first)}')
        p_itog=[]
        p_ohl=p_ohl_2
        while q <= len(rho_ohl)-2:
            p_itog.append(p_ohl + delta_p[q])
            p_ohl = p_ohl + (delta_p[q])
            q += 1
        second=p_itog
        print(f'second={len(second)}')
        p_itog = first + second
        print(f'p_itog={len(p_itog)}')
    else:
        p_itog.append(p_ohl)
        for deltaaaa_p in islice(delta_p, 0, len(delta_p)-1):
            p_itog.append(p_ohl+deltaaaa_p)
            p_ohl=p_ohl+(deltaaaa_p)


    # Создание DataFrame
    df = pd.DataFrame({
        'Re': Re,
        'epsilon':epsilon,
        'delta_p':delta_p,
        "d_sh_otn":delta_sheroh_otn,
        'l':l,
        'Re_gr':Re_gr
    })
    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table5.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
    print(f'Суммарные потери равны: {(max(p_itog)-min(p_itog))*0.000001:.3f} МПа')
    return delta_p,p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l
def tabl_6(T_st_g,T_st_ohl):
    # Создание DataFrame
    df = pd.DataFrame({
        'T_st_g': T_st_g,
        'T_st_ohl': T_st_ohl
    })
    # Замена NaN на прочерки
    df_filled = df.fillna('-')
    # Настройка отображения всех строк и столбцов
    df_filled.to_excel('table6.xlsx', index=False)  # Сохранить в Excel
    # Вывод таблицы
    print(df_filled)
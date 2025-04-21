"""
Модуль для взаимодействия с библиотекой Cantera.

Предполагается использовать для:
- Получения термодинамических свойств продуктов сгорания,
- Расчёта химического равновесия в КС и сопле,
- Вычисления параметров горючих/окислителей.

"""

import cantera as ct
import ast
def find_params_ks(gas,km0,alpha,H_gor,H_ok,fuel,oxidizer,p_k,T_st_g):
    # Преобразуем fuel, если он задан как строка
    if isinstance(fuel, str):
        fuel = ast.literal_eval(fuel)
    # То же для oxidizer
    if isinstance(oxidizer, str):
        oxidizer = ast.literal_eval(oxidizer)
    C_itog=[]
    km = km0 * alpha
    m_gor = 1 / (1 + km)
    m_ok = km / (1 + km)

    # Настройка газа один раз
    gas.set_equivalence_ratio(1 / alpha, fuel, oxidizer)
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')
    for T in T_st_g:
        if T is not None:
            gas.TP = T, p_k * 10 ** 6
            gas.equilibrate('TP')
            C_itog.append(gas.cp)
            print(gas.T,gas.cp)
    print('Расчет c_p окончен')
    return C_itog
def find_params_proverka(km0,alpha,H_gor,H_ok,fuel,oxidizer,p_k,T):
    if isinstance(fuel, str):
        fuel = ast.literal_eval(fuel)
    # То же для oxidizer
    if isinstance(oxidizer, str):
        oxidizer = ast.literal_eval(oxidizer)
    """--------------------Поиск всех основных параметров в камере сгорания--------------------"""
    k0 = km0
    # gas = ct.Solution('gri30_highT.yaml')
    gas = ct.Solution('gri30.yaml')
    km = k0 * alpha
    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000
    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)
    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')

    gas.TP = T, p_k * 10 ** 6
    gas.equilibrate('TP')

    T_1 = gas.T
    P_1 = gas.P
    V_1 = gas.v

    # расчёт равновесной Cp
    gas.TP = T_1 * 1.01, P_1
    gas.equilibrate('TP')
    H2 = gas.enthalpy_mass
    gas.TP = T_1 * 0.99, P_1
    gas.equilibrate('TP')
    H1 = gas.enthalpy_mass
    CPEQ = (H2 - H1) / (0.02 * T_1)
    return CPEQ
def find_params_tog(km0,alpha,H_gor,H_ok,fuel,oxidizer,p_k):
    if isinstance(fuel, str):
        fuel = ast.literal_eval(fuel)
    # То же для oxidizer
    if isinstance(oxidizer, str):
        oxidizer = ast.literal_eval(oxidizer)
    k0 = km0
    # gas = ct.Solution('gri30_highT.yaml')
    gas = ct.Solution('gri30.yaml')
    km = k0 * alpha
    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000
    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)
    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')
    gas.HP = H_sum, p_k * 10 ** 6
    gas.equilibrate('HP')

    # Запоминаем параметры в камере для удобства использования в последующих расчётах
    T_og = gas.T
    R_og = gas.cp - gas.cv
    c_p_T_0g=gas.cp
    dynamic_viscosity = gas.viscosity
    return T_og,R_og,c_p_T_0g,dynamic_viscosity

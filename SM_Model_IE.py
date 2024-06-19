import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def matlab2PythonDates(dateMatlab):
    days = dateMatlab % 1
    return datetime.fromordinal(int(dateMatlab)) + timedelta(days=days) - timedelta(days=366)

def kling_gupta_efficiency(sim, obs):
    valid_mask = ~np.isnan(sim) & ~np.isnan(obs)
    sim = sim[valid_mask]
    obs = obs[valid_mask]
    r = np.corrcoef(sim, obs)[0, 1]
    alpha = np.std(sim) / np.std(obs)
    beta = np.mean(sim) / np.mean(obs)
    kge = 1 - np.sqrt((r - 1)**2 + (alpha - 1)**2 + (beta - 1)**2)
    return kge

def SMestim_IE_02(PTSM, PAR, FIG, namefig):
    M = PTSM.shape[0]
    D = PTSM[:, 0]
    PIO = PTSM[:, 1]
    TEMPER = PTSM[:, 2]
    WWobs = PTSM[:, 3]
    dt = round(np.nanmean(np.diff(D)) * 24 * 10000) / 10000
    MESE = pd.to_datetime([matlab2PythonDates(d) for d in D]).month

    W_p = PAR[0]
    W_max = PAR[1]
    alpha = PAR[2]
    m2 = PAR[3]
    Ks = PAR[4]
    Kc = PAR[5]
    Ks = Ks * dt

    L = np.array([0.2100, 0.2200, 0.2300, 0.2800, 0.3000, 0.3100,
                  0.3000, 0.2900, 0.2700, 0.2500, 0.2200, 0.2000])
    Ka = 1.26
    EPOT = (TEMPER > 0) * (Kc * (Ka * L[MESE - 1] * (0.46 * TEMPER + 8) - 2)) / (24 / dt)

    WW = np.zeros(M)

    W = W_p * W_max
    for t in range(M):
        IE = PIO[t] * ((W / W_max) ** alpha)
        E = EPOT[t] * W / W_max
        PERC = Ks * (W / W_max) ** m2
        W = W + (PIO[t] - IE - PERC - E)
        if W >= W_max:
            SE = W - W_max
            W = W_max
        else:
            SE = 0
        WW[t] = W / W_max

    valid_mask = ~np.isnan(WW) & ~np.isnan(WWobs)
    WW_valid = WW[valid_mask]
    WWobs_valid = WWobs[valid_mask]

    RMSE = np.nanmean((WW_valid - WWobs_valid) ** 2) ** 0.5
    NS = 1 - np.nansum((WW_valid - WWobs_valid) ** 2) / np.nansum((WWobs_valid - np.nanmean(WWobs_valid)) ** 2)
    NS_radQ = 1 - np.nansum((np.sqrt(WW_valid + 0.00001) - np.sqrt(WWobs_valid + 0.00001)) ** 2) / \
                 np.nansum((np.sqrt(WWobs_valid + 0.00001) - np.nanmean(np.sqrt(WWobs_valid + 0.00001))) ** 2)
    NS_lnQ = 1 - np.nansum((np.log(WW_valid + 0.0001) - np.log(WWobs_valid + 0.0001)) ** 2) / \
                np.nansum((np.log(WWobs_valid + 0.0001) - np.nanmean(np.log(WWobs_valid + 0.0001))) ** 2)
    NS_lnQ = np.real(NS_lnQ)
    NS_radQ = np.real(NS_radQ)

    X = np.column_stack((WW_valid, WWobs_valid))
    RRQ = np.corrcoef(X, rowvar=False) ** 2
    RQ = RRQ[1, 0]

    KGE = kling_gupta_efficiency(WW_valid, WWobs_valid)

    return WW, NS, KGE

def plot_results(D, WW, WWobs, PIO, NS, NS_lnQ, NS_radQ, RQ, RMSE, KGE, namefig):
    D_dates = [matlab2PythonDates(d) for d in D]

    plt.figure(figsize=(10, 7))
    
    s = f'NS= {NS:.3f} NS(lnSD)= {NS_lnQ:.3f} NS(radSD)= {NS_radQ:.3f} RQ= {RQ:.3f} RMSE= {RMSE:.3f} KGE= {KGE:.3f}'
    
    ax1 = plt.axes([0.1, 0.5, 0.8, 0.40])
    ax1.set_title(s, fontsize=14, fontweight='bold')
    ax1.plot(D_dates, WWobs, 'g', linewidth=3, label=r'$\theta_{obs}$')
    ax1.plot(D_dates, WW, 'r', linewidth=2, label=r'$\theta_{sim}$')
    ax1.legend()
    ax1.set_ylabel('Relative Soil Moisture [-]')
    ax1.grid(True)
    ax1.set_xlim([D_dates[0], D_dates[-1]])
    y_min = np.nanmin(WWobs[np.isfinite(WWobs)]) - 0.05
    y_max = np.nanmax(WWobs[np.isfinite(WWobs)]) + 0.05
    ax1.set_ylim([y_min, y_max])
    ax1.tick_params(labelbottom=False)  

    ax2 = plt.axes([0.1, 0.1, 0.8, 0.40])
    ax2.plot(D_dates, PIO, color=[.5, .5, .5], linewidth=3)
    ax2.set_ylabel('Rain (mm/h)')
    ax2.grid(True)
    ax2.set_xlim([D_dates[0], D_dates[-1]])
    ax2.set_ylim([0, 1.05 * np.nanmax(PIO[np.isfinite(PIO)])])
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%Y-%m-%d')))

    plt.savefig(namefig, format='png', dpi=150)
    plt.show()



PTSM = np.loadtxt("C:/Users/h.mosaffa/Desktop/SSMODEL/data.txt")
PAR = np.loadtxt("C:/Users/h.mosaffa/Desktop/SSMODEL/Xopt.txt")
FIG = 1
namefig = 'C:/Users/h.mosaffa/Desktop/SSMODEL/figure.png'

WW, NS, KGE = SMestim_IE_02(PTSM, PAR, FIG, namefig)

if FIG == 1:
    D = PTSM[:, 0]
    PIO = PTSM[:, 1]
    TEMPER = PTSM[:, 2]
    WWobs = PTSM[:, 3]

    valid_mask = ~np.isnan(WW) & ~np.isnan(WWobs)
    WW_valid = WW[valid_mask]
    WWobs_valid = WWobs[valid_mask]
    
    RMSE = np.nanmean((WW_valid - WWobs_valid) ** 2) ** 0.5
    NS_lnQ = 1 - np.nansum((np.log(WW_valid + 0.0001) - np.log(WWobs_valid + 0.0001)) ** 2) / \
                np.nansum((np.log(WWobs_valid + 0.0001) - np.nanmean(np.log(WWobs_valid + 0.0001))) ** 2)
    NS_radQ = 1 - np.nansum((np.sqrt(WW_valid + 0.00001) - np.sqrt(WWobs_valid + 0.00001)) ** 2) / \
                 np.nansum((np.sqrt(WWobs_valid + 0.00001) - np.nanmean(np.sqrt(WWobs_valid + 0.00001))) ** 2)
    NS_lnQ = np.real(NS_lnQ)
    NS_radQ = np.real(NS_radQ)
    
    X = np.column_stack((WW_valid, WWobs_valid))
    RRQ = np.corrcoef(X, rowvar=False) ** 2
    RQ = RRQ[1, 0]
    
    plot_results(D, WW, WWobs, PIO, NS, NS_lnQ, NS_radQ, RQ, RMSE, KGE, namefig)


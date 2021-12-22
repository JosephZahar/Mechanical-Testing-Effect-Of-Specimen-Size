import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import numpy as np
import seaborn as sns

Large_df = pd.read_excel(r'/Users/macbookpro/Desktop/Mech test.xlsx', sheet_name='Large')
Small_df = pd.read_excel(r'/Users/macbookpro/Desktop/Mech test.xlsx', sheet_name='Small')
Specimens = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def Tangent_Stiffness_15(data, n):
    Strain_13 = data.loc[data['Compressive strain (Extension) ' + n] >= 0.13].head(1)
    Strain_18 = data.loc[data['Compressive strain (Extension) ' + n] >= 0.18].head(1)
    Tangent_Stiffness = ((Strain_18['Load ' + n].values - Strain_13['Load ' + n].values) / (
            Strain_18['Compressive extension ' + n].values - Strain_13['Compressive extension ' + n].values))
    return Tangent_Stiffness

def Tangent_Modulus_15(data, n):
    Strain_13 = data.loc[data['Compressive strain (Extension) ' + n] >= 0.13].head(1)
    Strain_18 = data.loc[data['Compressive strain (Extension) ' + n] >= 0.18].head(1)
    Tangent_Modulus = (
            (Strain_18['Compressive stress ' + n].values - Strain_13['Compressive stress ' + n].values) / 0.15)
    return Tangent_Modulus

T1 = {i: [Tangent_Stiffness_15(Small_df, i), Tangent_Modulus_15(Small_df, i)] for i in Specimens}
T1 = pd.DataFrame(T1, columns= Specimens, index=['Tangent Stiffness (N/mm)', 'Tangent Modulus (N/mm^2)'])
T1.to_csv('Small diameter sample.csv')

T2 = {i: [Tangent_Stiffness_15(Small_df, i), Tangent_Modulus_15(Small_df, i)] for i in Specimens}
T2 = pd.DataFrame(T2, columns= Specimens, index=['Tangent Stiffness (N/mm)', 'Tangent Modulus (N/mm^2)'])
T2.to_csv('Large diameter sample.csv')

Tangent_Stiffness_large = [Tangent_Stiffness_15(Large_df, i) for i in Specimens]
Tangent_Stiffness_small = [Tangent_Stiffness_15(Small_df, i) for i in Specimens]
Tangent_Modulus_large = [Tangent_Modulus_15(Large_df, i) for i in Specimens]
Tangent_Modulus_small = [Tangent_Modulus_15(Small_df, i) for i in Specimens]

Stiffness_mean_small, Stiffness_mean_large, Modulus_mean_small, Modulus_mean_large = np.mean(
    Tangent_Stiffness_small), np.mean(Tangent_Stiffness_large), np.mean(Tangent_Modulus_small), np.mean(
    Tangent_Modulus_large)
Stiffness_STDV_small, Stiffness_STDV_large, Modulus_STDV_small, Modulus_STDV_large = np.std(
    Tangent_Stiffness_small), np.std(Tangent_Stiffness_large), np.std(Tangent_Modulus_small), np.std(
    Tangent_Modulus_large)

TTEST_Stiffness = stats.ttest_ind(Tangent_Stiffness_small,Tangent_Stiffness_large)
TTEST_Modulus = stats.ttest_ind(Tangent_Modulus_small,Tangent_Modulus_large)

T3 = {'mean': ['Tangent Stiffness (N/mm)', Stiffness_mean_small, Stiffness_mean_large, TTEST_Stiffness[1]],
      'standard deviation': ['Tangent Stiffness (N/mm)', Stiffness_STDV_small, Stiffness_STDV_large,'']}
T3 = pd.DataFrame(T3, columns=['mean', 'standard deviation'],
                  index=['Sample 1 Name', 'Small diameter sample', 'Large diameter sample','Students T test, p value'])
T3.to_csv('STIFFNESS.csv')

T4 = {'mean': ['Tangent Modulus (N/mm^2)', Modulus_mean_small, Modulus_mean_large, TTEST_Modulus[1]],
      'standard deviation': ['Tangent Modulus (N/mm^2)', Modulus_STDV_small, Modulus_STDV_large, '']}
T4 = pd.DataFrame(T4, columns=['mean', 'standard deviation'],
                  index=['Sample 1 Name', 'Small diameter sample', 'Large diameter sample','Students T test, p value'])
T4.to_csv('MODULUS.csv')

data = {'Sample': ['Small diameter sample', 'Large diameter sample'],
        'Tangent Stiffness (N/mm)': [Stiffness_mean_small, Stiffness_mean_large],
        'Tangent Modulus (N/mm^2)': [Modulus_mean_small, Modulus_mean_large]}

fonttype = {'fontname': 'Times New Roman'}
fig = plt.figure()
ax = fig.add_subplot(121)
ax.bar('Sample', 'Tangent Stiffness (N/mm)', data=data, yerr=[Stiffness_STDV_small, Stiffness_STDV_large], linewidth=0.5, facecolor="dimgrey",
       edgecolor="black", capsize=2, width=0.7)
ax.set_ylabel('Tangent Stiffness (N/mm)', fontsize=9, **fonttype)
ax.set_xlabel('')
for tick in ax.get_xticklabels():
    tick.set_fontname("Times New Roman")
for tick in ax.get_yticklabels():
    tick.set_fontname("Times New Roman")
sns.despine()

ax2 = fig.add_subplot(122)
ax2.bar('Sample', 'Tangent Modulus (N/mm^2)', data=data,yerr=[Modulus_STDV_small, Modulus_STDV_large],  linewidth=0.5, facecolor="dimgrey",
        edgecolor="black", capsize=2, width=0.7)
ax2.set_ylabel('Tangent Modulus (N/mm^2)', fontsize=9, **fonttype)
ax2.set_xlabel('')
for tick in ax2.get_xticklabels():
    tick.set_fontname("Times New Roman")
for tick in ax2.get_yticklabels():
    tick.set_fontname("Times New Roman")
sns.despine()
plt.tight_layout(pad=2.5)
plt.show()
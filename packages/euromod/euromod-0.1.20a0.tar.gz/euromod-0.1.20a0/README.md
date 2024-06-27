# Euromod Connector 

The Euromod Connector for Python is built to facilitate and simplify the usage of the [EUROMOD](https://euromod-web.jrc.ec.europa.eu "https://euromod-web.jrc.ec.europa.eu") microsimulation model for research and analysis purposes. The Euromod Conector for Python is a library providing tools for running simulations and interacting with EUROMOD.
EUROMOD is a tax-benefit microsimulation model for the European Union that enables researchers and policy analysts to calculate, in a comparable manner, the effects of taxes and benefits on household incomes and work incentives for the population of each country and for the EU as a whole. It is a static microsimulation model that applies user-defined tax and benefit policy rules to harmonised microdata on individuals and households, calculates the effects of these rules on household income, and then outputs results at the micro level. The default policy rules are those set to 30 June for a given poicy year and the microdata are processed according to a standard set of protocols. 
EUROMOD aims to simulate as much as possible of the tax and benefit components of households disposable income and other policy instruments such as income taxes, social contributions, family benefits, housing benefits, social assistance and other income-related benefits.


## Installation 
Install via [PyPi](https://test.pypi.org/project/euromod/)  using _pip_:
```bash
$ pip install euromod
```

### Requirements
The Euromod Connector requires two [EUROMOD](https://euromod-web.jrc.ec.europa.eu "https://euromod-web.jrc.ec.europa.eu") components: 1) the model (coded policy rules) , and 2) the input microdata with the variables that respect the [EUROMOD](https://euromod-web.jrc.ec.europa.eu "https://euromod-web.jrc.ec.europa.eu") naming conventions.
For more information, please, read the sections "Model" and "Input microdata" on the [Download Euromod](https://euromod-web.jrc.ec.europa.eu/download-euromod "https://euromod-web.jrc.ec.europa.eu/download-euromod") web page.


## Simulation

Importing and loading the model:

```python
In[1]: from euromod import Model
In[2]: mod=Model(r"C:\EUROMOD_RELEASES_I6.0+")
```

Loading the dataset using pandas:
```python
In[3]: import pandas as pd
In[4]: data = pd.read_csv(r"C:\EUROMOD_RELEASES_I6.0+\Input\sl_demo_v4.txt",sep="\t")
```

Running a simulation on system 'SL_1996' of the country Simpleland 'SL' (Note: this country model is provided by default with the EUROMOD project):
```python
In[5]: out=mod['SL']['SL_1996'].run(data,'sl_demo_v4')
In[6]: out.outputs[0]
```
```python
Out[1]:
       idhh  idperson  idmother  ...    ils_dispy  il_taxabley  il_bsa_base
0       1.0     101.0       0.0  ...   807.018500      0.00000    807.01850
1       1.0     102.0       0.0  ...     0.000000      0.00000      0.00000
2       1.0     103.0     102.0  ...     0.000000      0.00000      0.00000
3       1.0     104.0     102.0  ...   934.294772    149.54786    149.54786
4       2.0     201.0       0.0  ...  1337.268280   1421.58535   1337.26828
    ...       ...       ...  ...          ...          ...          ...
1255  500.0   50003.0   50002.0  ...     0.000000      0.00000      0.00000
1256  500.0   50004.0   50002.0  ...     0.000000      0.00000      0.00000
1257  500.0   50005.0   50002.0  ...     0.000000      0.00000      0.00000
1258  500.0   50006.0       0.0  ...   839.845300      0.00000    839.84530
1259  500.0   50007.0       0.0  ...     0.000000      0.00000      0.00000

[1260 rows x 43 columns]
```

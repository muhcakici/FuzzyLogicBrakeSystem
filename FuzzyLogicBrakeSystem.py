import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as karar
#degiskenlerin oluşturulması ve aralıklarının belirlenmesi
pedal=karar.Antecedent(np.arange(0,101,1),'pedal')
speed=karar.Antecedent(np.arange(0,101,1),'hiz' )
brake=karar.Consequent(np.arange(0,101,1), 'fren')

#üyelik fonksiyonlarının oluşturulması
pedal['az']=fuzz.trimf(pedal.universe,[0,0,50])
pedal['normal']=fuzz.trimf(pedal.universe,[0,50,100])
pedal['fazla']=fuzz.trimf(pedal.universe,[50,100,100])

speed['az']=fuzz.trimf(speed.universe,[0,0,60])
speed['normal']=fuzz.trimf(speed.universe,[20,50,80])
speed['fazla']=fuzz.trimf(speed.universe,[40,100,100])

brake['zayif']=fuzz.trimf(brake.universe, [0,0,100])
brake['guclu']=fuzz.trimf(brake.universe, [0,100,100])

#görsellestirme
pedal.view()
speed.view()
brake.view()

#kuralların belirlenmesi
kural1=karar.Rule(pedal['normal'] , brake['guclu'])
kural2=karar.Rule(pedal['fazla'] & speed['fazla'] ,brake['guclu'])
kural3=karar.Rule(pedal['az'] | speed['az'] ,brake['zayif'])
kural4=karar.Rule(pedal['az'] , brake['zayif'])

#birlesim kumelerinin olusturulması
sonuc_karar=karar.ControlSystem([kural1,kural2,kural3,kural4])
sonuc_=karar.ControlSystemSimulation(sonuc_karar)

#girdiler
sonuc_.input['pedal']=40
sonuc_.input['hiz']=75

#sonuc ve gorsellesitirme
sonuc_.compute()
print("Performans:",sonuc_.output['fren'])
pedal.view(sim=sonuc_)
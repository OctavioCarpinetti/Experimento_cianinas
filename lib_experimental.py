import numpy as np
import matplotlib.pyplot as plt
import scipy.odr as sci

# Se define la clase Datos que es la que se suele importar
class Datos:
  def __init__(self,datosx,datosy):
    # Cuando se define un objeto de la clase datos, se ejecuta __init__, entrando en la clase, los parámetros que se insertan al definirse. En este caso
    # en la inicialización, se toman datosx, datosy, y se define una variable que contendrá eventualmente las variables que se ajusten.
    self.resultado_ajuste="No se ejecutó el método .ajustar()"
    self.datosx=datosx
    self.datosy=datosy

  # Esta función es de uso exclusivo dentro de la clase, y se usa eventualmente para calcular xi cuadrado en el método chicuad.
  def calc_xi(f,A,x,y):
    ji=0
    for i in range(len(x)):
      ji+=(y[i]-f(A,x[i]))**2
    return ji/(len(x)-1)

  # Los siguientes son métodos de la clase; es decir funciones que se pueden ejecutar sobre una instancia de la misma.

  # ajustar es el método principal, que hace ajustes dada una función con parámetros y un valor inicial.
  def ajustar(self,funcion,valor_inicial=[1],errorx=None,errory=None):
    modelo=sci.Model(funcion)
    misdatos=sci.Data(self.datosx,self.datosy)
    miodr=sci.ODR(misdatos,modelo,beta0=valor_inicial)
    mioutput=miodr.run()
    self.resultado_ajuste=mioutput.beta
    self.error_ajuste=mioutput.sd_beta
    self.funcion=funcion
    return self.resultado_ajuste

  # graficar_datos es un método que grafica los datos de la clase, x contra y.
  def graficar_datos(self,acumular=False):
    plt.plot(self.datosx,self.datosy,".")
    plt.grid()
    if not acumular:
      plt.show()

  # graficar_con_ajuste grafica los datos junto con el ajuste realizado si ya se ejecutó del método .ajustar, de otro modo avisa.
  def graficar_con_ajuste(self,errorx,errory,acumular=False,eje_x="",eje_y="",nombre_datos="",nombre_ajuste="",titulo="",color_datos=None,color_ajuste=None,formato=","):
    if not isinstance(self.resultado_ajuste,str):
      plt.errorbar(self.datosx,self.datosy,xerr=errorx,yerr=errory,fmt=formato,capthick=1,capsize=0,elinewidth=1,label=nombre_datos,color=color_datos)
      xaj=np.linspace(min(self.datosx),max(self.datosx),1000)
      yaj=self.funcion(self.resultado_ajuste,xaj)
      plt.plot(xaj,yaj,label=nombre_ajuste,color=color_ajuste)
      plt.title(titulo)
      plt.xlabel(eje_x)
      plt.ylabel(eje_y)
      plt.grid()
      # Por defecto acumular es False, y por tanto el método muestra un gráfico solo. Si acumular es True, el gráfico se agrega a la superposición de gráficos.
      if not acumular:
        plt.show()
    else:
      print(self.resultado_ajuste)
      pass

  # chcuad calcula el valor de xi cuadrado, si ya se ejecutó el método .ajuste, de otro modo avisa.
  def chicuad(self):
    if not isinstance(self.resultado_ajuste,str):
      return Datos.calc_xi(self.funcion,self.resultado_ajuste,self.datosx,self.datosy)
    else:
      print(self.resultado_ajuste)
      pass

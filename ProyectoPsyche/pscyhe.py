import nltk
import spacy 
nlp=spacy.load("es_core_news_sm")
#from nltk.classify.scikitlearn import SklearnClassifier
# from sklearn.naive_bayes import MultinomialNB
from itertools import chain
import joblib 
import random
#from nltk import NaiveBayesClassifier as nbc
import os

with open("ProyectoPsyche\corpus finales\Entrenamieto(pos,neu,neg).txt","r", encoding="utf-8") as b:
  ent_posneg = b.read()
#print(ent_posneg)
with open("ProyectoPsyche\corpus finales\Recomendaciones(ansiedad).txt","r", encoding="utf-8") as c:
  rec_ans = c.read()
#print(rec_ans)
with open("ProyectoPsyche\corpus finales\Recomendaciones(depresion).txt","r", encoding="utf-8") as d:
  rec_dep = d.read()
#print(rec_dep)
with open('ProyectoPsyche\corpus finales\Recomendaciones(adiccion).txt','r', encoding="utf-8") as e:
  rec_adc = e.read()
#print(rec_adc)
with open('ProyectoPsyche\corpus finales\Buscar(informacion).txt','r', encoding="utf-8") as inf:
  info = inf.read()
#print(info)
with open('ProyectoPsyche\corpus finales\Contactos(bienestarUN).txt','r', encoding="utf-8") as cont:
  contac = cont.read()
#print(contac)
with open('ProyectoPsyche\corpus finales\Entrenamieto(enfermedades).txt','r', encoding="utf-8") as g:
  ent_enf2 = g.read()
#print(ent_enf2)

def respuesta():
  return input('')

def nombre(txt): 
  s = ''
  n = len(txt)
  if txt[n-1] == " ":
    n -= 1
  while n>0 and txt[n-1] != " ":
    if txt[n-1] != ".":
      s += txt[n-1]
    n-=1
  return s[::-1]

def estudiante(txt2):
  txt = txt2.lower()
  if txt == 'si' or txt == 'sí':
    flag = True
  elif txt == 'no':
    flag = False
  else:
    print('Disculpa no te entendí, por favor repiteme Si o No')
    txt = input('')
    return estudiante(txt)
  return flag

def preguntas(txt):
  n = len(txt)
  i = 0
  while i<n and txt[i] != '?' and txt[i] !='¿':
    i += 1
  return  i < n

def stopw_tok(txt,stopw):
  s = ''
  txt_tok = nltk.word_tokenize(txt.lower())
  bag = filter(lambda word: word not in stopw, txt_tok)
  for i in bag:
    s += i + " "
  return s

def lematiza(txt):
  palabras = nlp(txt)
  return palabras

def formato(txt):
  tok_par = nltk.tokenize.blankline_tokenize(txt)
  n = len(tok_par)
  for i in range(n):
    sent = nltk.sent_tokenize(tok_par[i])
    tok_par[i] = sent
  return tok_par

def vocabulario(matriz):
  voc = set(chain(*[nltk.word_tokenize(i[0]) for i in matriz]))
  return voc

def bagwordsentrena(matriz,voc):
  x = [({i:(i in nltk.word_tokenize(sent)) for i in voc},tag) for sent,tag in matriz]
  return x

def bagwords(txt,voc):
  x = {i:(i in nltk.word_tokenize(txt)) for i in voc} 
  return x

def neutralidad(resultado1,resultado2):
  if (resultado1 == 'pos' and resultado2 == 'pos'):
    return 1
  elif resultado1 != resultado2:
    return 0
  else:
    return -1

def enfermedad(respuesta, x ,y,z):
  if respuesta == 'dep':
    x += 1
  elif respuesta == 'ans':
    y += 1
  elif respuesta == 'adc':
    z += 1
  return x,y,z

def clasifica(txt1,txt2):
  if txt1 == txt2:
    return txt1
  else: 
    return ''

def main():
  os.system('mode con: cols=200 lines=100')
  clasificadornb = joblib.load('ProyectoPsyche\corpus finales\clasnbPOSNEG.joblib.pkl')
  SKclasificador = joblib.load('ProyectoPsyche\corpus finales\clasSKPOSNEG.joblib.pkl') 
  clasificadornbenf = joblib.load('ProyectoPsyche\corpus finales\clasnbENF.joblib.pkl')
  SKclasificadorenf = joblib.load('ProyectoPsyche\corpus finales\clasSKENF.joblib.pkl') 
  resp_inf = formato(info)
  os.system("cls")
  print('PSYCHE: ¡Hola! Soy Psyche, tu asistente de Psicoayuda. Estoy aquí para ayudarte y escucharte ¿Cuál es tu nombre?')
  print('Tú: ', end="")
  r = respuesta()
  nom = nombre(r)
  os.system("cls")
  print('PSYCHE: mucho gusto {}, ¿Eres estudiante de la UN? Dime Si o No '.format(nom))
  print(nom, end=": ")
  e = respuesta()
  est = estudiante(e)
  os.system("cls")
  print("PSYCHE: ",resp_inf[0][random.randint(0,9)])
  print('PSYCHE: si ya no quieres hablar conmigo, puedes decirme adios')
  print(nom, end=": ")
  f = respuesta()
  os.system("cls")
  stopw = set(nltk.corpus.stopwords.words('spanish'))
  stopw.update([".",",","(","]"])
  f_posneg = formato(ent_posneg)
  vocpos = vocabulario(f_posneg)
  f_enfer = formato(ent_enf2)
  vocenfer = vocabulario(f_enfer)
  #analisador3 = SentimentIntensityAnalyzer()
  x,y,z = 0,0,0
  while x<3 and y<3 and z<3 and f != 'adios':
    sinstop = stopw_tok(f,stopw)
    lema = str(lematiza(sinstop))
    bg = bagwords(lema,vocpos)
    clas1 = str(clasificadornb.classify(bg))
    clas2 = str(SKclasificador.classify(bg))
    #analisador3 = SentimentIntensityAnalyzer()
    #clas3 = analisador3.polarity_scores(f)
    aux = neutralidad(clas1,clas2) 
    total = aux #+ clas3['compound']
    if total < 0:
       bg2 = bagwords(lema,vocenfer)
       enf1 = clasificadornbenf.classify(bg2)
       enf2 = SKclasificadorenf.classify(bg2)
       flagtxt = clasifica(enf1,enf2)
       #print(flagtxt)
       x,y,z = enfermedad(flagtxt,x,y,z)
       #print(x,y,z)
       print('PSYCHE: ',resp_inf[1][random.randint(0,18)])
    else:
      print('PSYCHE: ',resp_inf[0][random.randint(0,17)])
    if preguntas(f):
      print('PSCYCHE:',resp_inf[2][random.randint(0,3)])
    print(nom, end=": ")
    f = respuesta()
    os.system("cls")
  if f == 'adios':
    print("PSYCHE: Que tengas un buen día. Un placer hablar contigo")
  elif x == 3:
    resp_dep = nltk.tokenize.blankline_tokenize(rec_dep)
    print('PSYCHE: ', resp_dep[random.randint(0,3)])
  elif y == 3:
    resp_ans = nltk.tokenize.blankline_tokenize(rec_ans)
    print('PSYCHE:', resp_ans[random.randint(0,3)])
  else:
    resp_adc = nltk.tokenize.blankline_tokenize(rec_adc)
    print('PSYCHE: ', resp_adc[random.randint(0,2)])
  if est and f != 'adios':
    rep_cont = nltk.tokenize.blankline_tokenize(contac)
    print('PSYCHE: ', rep_cont[random.randint(0,5)])
main()

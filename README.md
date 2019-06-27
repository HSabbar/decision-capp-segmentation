# Segmentation de décision avec l'apprentissage supervisé

Ce modèle de l'apprentissage consiste de découper des décisions jurisprudences en macro (Entête, Expose litige, Motif de la décision, Dispositif) et en micro (des arguments Sous motif de la décision) il est basé sur l'algorithme de **RNN** en utilisent **LSTM Bidirectional**    


## Créer l'environnement :
```
conda create -n textseg_3 python=3.7 numpy scipy gensim ipython 
source activate textseg_3
pip3 install torch tqdm pathlib2 segeval tensorboard_logger flask  
pip3 install nltk pandas xlrd xlsxwriter termcolor flask_wtf
```
## Exécuter le processus d'apprentissage :
### PATH DataSet :
Ajouter le chemin vres le DataSet d'apprentissage dans le fichier **configgenerator.py** et puis exécuter :

`python3 configgenerator.py` 

### Lancer l'apprentissage : 
```
python3 run.py --cuda --model max_sentence_embedding
```

## Évaluer le modèle : 

```
python3 test_accuracy.py --cuda --model Model-data-5517/Meilleur_model.t7
```

## Exécuter le modèle sur des décisions : 

```
python3 visualize_model_seg.py --model Model-data-5517/Meilleur_model.t7 --file webapp/Fpath_Testing.txt --output webapp/out/
```
`--file`: Contient les chemins vres décisions à découper 

`--output`: Contiendra les décisions découpé 





import natural_selection_neurone as neuro
import pickle

if __name__=='__main__':
    anim=neuro.Animal()
    f=open("test.pkl",'wb')
    pickle.dump(anim,f)
    f.close()
    f=open("test.pkl","rb")
    pickled_anim=pickle.load(f)
    f.close()

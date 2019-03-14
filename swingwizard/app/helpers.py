from fastai import *
from fastai.vision import *
import pims
import av
from flask import *
from config import *
from werkzeug.utils import *

UPLOAD_FOLDER = basedir+'/app/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'])

PTH_DIR    = Path('.') # /models in root dir
PTH_NAME   = '3_13'
IMG_DIR    = UPLOAD_FOLDER
CLASSES    = ['bad swing','good swing']
RESNET     = 50
NORMALIZER = imagenet_stats
TRANSFORMS = get_transforms()


class ImageClassifier(object):
    def __init__(self):
        self.learner = self.setup_model(PTH_DIR, PTH_NAME, CLASSES, RESNET, TRANSFORMS, NORMALIZER)

    def setup_model(self, pth_dir=PTH_DIR, pth_name=PTH_NAME, classes=CLASSES, resnet=RESNET, tfms=TRANSFORMS, normalizer=NORMALIZER, **kwargs):
        data = (ImageDataBunch
                .single_from_classes(pth_dir, classes, tfms, **kwargs)
                .normalize(normalizer))
        learn = create_cnn(data, self.get_resnet(resnet), pretrained=False)
        learn.load(pth_name)
        return learn

    def get_resnet(self, resnet=RESNET):
        return getattr(models, f'resnet{resnet}')

    def predict(self, img):
        img = open_image(img)
        pred_class, pred_idx, losses = self.learner.predict(img)
        c = f'{losses.numpy()[1]*100:.2f}'
        return pred_class,c


M = ImageClassifier().predict


def get_results(frameLST,frame):
  p1,c1 = M(frameLST[frame])
  return p1,c1


def select_frames(l):
    f1 = l[:1][0]
    quarter = float(len(l))/4
    f2 = (l[int(quarter+.5)] if quarter%2 !=0 else l[int(quarter)])
    mid = float(len(l))/2
    f3 = (l[int(mid-.5)] if mid%2 !=0 else l[int(mid)])
    threeq = float(len(l))*.75
    f4 = (l[int(threeq-.5)] if threeq%2 !=0 else l[int(threeq)])
    f5 = l[-1]
    return [f1,f2,f3,f4,f5]


def get_frames(fp,save=True,show=False):
    vp = av.open(fp)
    l1 = [frame.to_image() for frame in vp.decode(video=0)]
    l2 = select_frames(l1)
    if save==True:
      i=1
      for x in l2:
        x.save(fp.replace('.mp4','')+'-'+f'{i}'+'.jpg')
        i+=1
    if show==True:
      l3 = [x.show() for x in l2]
      return l3
    return l2


def get_filename(fp,save=True):
  if 'file' not in request.files:
    flash('No file part')
    return redirect(request.url)
  file = request.files['file']
  if file.filename == '':
    flash('No selected file')
    return redirect(request.url)
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    if save==True:
      file.save(os.path.join(fp, filename))
    fl = os.path.join(fp, filename)
  return fl


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

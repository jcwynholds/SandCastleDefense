import pygame, os, sys

class EventedSprite(pygame.sprite.DirtySprite):
  def __init__(self):
    pygame.sprite.DirtySprite.__init__(self)
    self.selected = False
    self.mouse = {
      'down': False,
      'over': False
    }

  def update(self, events):
    self.checkState(events)

  def mousemove(self, event):
    pos = pygame.mouse.get_pos()
    if self.rect.collidepoint(pos):
      self.on_mousemove(event)
    else:
      if self.mouse['over']:
        self.on_mouseout(event)
      self.mouse['over'] = False

  def mouseover(self):
    pos = pygame.mouse.get_pos()
    if self.rect.collidepoint(pos):
      self.on_mouseover()
      self.mouse['over'] = True
    
  def click(self, event):
    self.on_click(event)

  def mousedown(self, event):
    if self.mouse['over']:
      self.on_mousedown(event)
      self.mouse['down'] = True

  def mouseup(self, event):
    if self.mouse['over']:
      self.on_mouseup(event)
      if self.mouse['down']:
        self.click(event)
    self.mouse['down'] = False

  def mousehold(self, event):
    if self.mouse['over'] and self.mouse['down']:
      self.on_mousehold(event)

  def checkState(self, events = []):
    self.mouseover()
    for event in events:
      if event.type == pygame.QUIT:
        # probably are you sure you want to quit
        sys.exit()
      if event.type == pygame.MOUSEMOTION:
        self.mousemove(event)
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          self.mousedown(event)
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          self.mouseup(event)

  def on_mousedown(self, event):
    return 0
  def on_mouseup(self, event):
    return 0
  def on_mousemove(self, event):
    return 0
  def on_mouseover(self):
    return 0
  def on_mouseout(self, event):
    return 0
  def on_click(self, event):
    return 0

class World(pygame.Surface, EventedSprite):
  _selected = None
  _instance = None
  _selection_changed = False
  structures = None  
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(World, cls).__new__(
                          cls, *args, **kwargs)
    return cls._instance

  def __init__(self, size):
    pygame.Surface.__init__(self, size)
    self.selected = False
    self.mouse = {
      'down': False,
      'over': False
    }
    self._supress = False
    self.rect = self.get_rect()

  def stop_event_propogation(self):
    self._supress = True

  def selection_changed(self):
    self._selection_changed = True

  def has_selected(self):
    return self._selected != None

  def set_selected(self, selectable):
    self._selected = selectable
    self.selection_changed()

  def clear_selected(self, selectable = None):
    if selectable == None or self._selected == selectable:
      self._selected = None
      self.selection_changed()

  def get_selected(self):
    return self._selected

  def update(self, events):
    if self._supress == True:
      self._supress = False
      return
    self.checkState(events)

  def on_click(self, event):
    if self._selected != None:
      self._selected.selected_update(event)
    self._selection_changed = False


class EventedSurface(pygame.Surface, EventedSprite):
  def __init__(self, size):
    pygame.Surface.__init__(self, size)
    self.selected = False
    self.mouse = {
      'down': False,
      'over': False
    }
    self.rect = self.get_rect()

class EventedShape(pygame.Surface, EventedSprite):
  def __init__(self):
    pygame.Rect.__init__(self)
    self.selected = False
    self.mouse = {
      'down': False,
      'over': False
    }
    self.rect = self


def load_image(name, colorkey=None):
  fullname = os.path.join(name)
  try:
    image = pygame.image.load(fullname)
  except pygame.error, message:
    print 'Cannot load image:', name
    raise SystemExit, message
  return image, image.get_rect()

def load_sliced_sprites(self, w, h, filename):
  '''
  Specs :
    Master can be any height.
    Sprites frames width must be the same width
    Master width must be len(frames)*frame.width
  Assuming you ressources directory is named "ressources"
  '''
  images = []
  master_image = pygame.image.load(os.path.join('.', filename)).convert_alpha()

  master_width, master_height = master_image.get_size()
  for j in xrange(int(master_height/h)):
    t = []
    images.append(t)
    for i in xrange(int(master_width/w)):
      position = (i*w,j*h,w,h)
      surf = master_image.subsurface(position)
      images[j].append(surf)
  return images
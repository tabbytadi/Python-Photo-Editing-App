import wx
from PIL import Image
from PIL import ImageFilter

class Example(wx.Frame):
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)
        pnl = wx.Panel(self)

        self.originalImage = Image.open('poster.jpg')
        self.filteredImage = self.originalImage.copy()
        self.image = wx.EmptyImage(self.filteredImage.size[0], self.filteredImage.size[1])
        self.image.SetData(self.filteredImage.convert("RGB").tobytes())
        self.image.SetAlpha(self.filteredImage.convert("RGBA").tobytes()[3::4])
        self.bitmap = wx.Bitmap(self.image)
        self.img = wx.StaticBitmap(pnl, 0, self.bitmap, pos=(400, 50))

        filters = ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SMOOTH',
                   'SMOOTH_MORE', 'SHARPEN']
        self.combo = wx.ComboBox(pnl, pos=(10, 180), size=(200, -1), choices=filters)
        self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)

        self.mirror_btn = wx.Button(pnl, label='Mirror', pos=(10, 20))
        self.mirror_btn.Bind(wx.EVT_BUTTON, self.OnMirror)

        self.rotate_btn = wx.Button(pnl, label='Rotate 90°', pos=(10, 50))
        self.rotate_btn.Bind(wx.EVT_BUTTON, self.OnRotate90)

        wx.StaticText(pnl, label="Rotate manually in degrees:", pos=(10, 80))
        self.rotate_degrees_text = wx.TextCtrl(pnl, pos=(190, 80), size=(70, -1))
        self.rotate_degrees_btn = wx.Button(pnl, label='Rotate', pos=(270, 80))
        self.rotate_degrees_btn.Bind(wx.EVT_BUTTON, self.OnRotateDegrees)

        wx.StaticText(pnl, label="Left:", pos=(10, 110))
        self.left_text = wx.TextCtrl(pnl, pos=(60, 110), size=(70, -1))
        wx.StaticText(pnl, label="Upper:", pos=(140, 110))
        self.upper_text = wx.TextCtrl(pnl, pos=(190, 110), size=(70, -1))
        self.crop_btn = wx.Button(pnl, label='Crop', pos=(270, 110))
        self.crop_btn.Bind(wx.EVT_BUTTON, self.OnCrop)

        wx.StaticText(pnl, label="Width:", pos=(10, 140))
        self.width_text = wx.TextCtrl(pnl, pos=(60, 140), size=(70, -1))
        wx.StaticText(pnl, label="Height:", pos=(140, 140))
        self.height_text = wx.TextCtrl(pnl, pos=(190, 140), size=(70, -1))
        self.resize_btn = wx.Button(pnl, label='Resize', pos=(270, 140))
        self.resize_btn.Bind(wx.EVT_BUTTON, self.OnResize)

        self.export_btn = wx.Button(pnl, label='Save Image As', pos=(10, 370))
        self.export_btn.Bind(wx.EVT_BUTTON, self.OnExportImage)

        self.undo_btn = wx.Button(pnl, label='Undo All Changes', pos=(10, 410))
        self.undo_btn.Bind(wx.EVT_BUTTON, self.OnUndo)

        self.SetSize((640, 480))
        self.SetTitle('Photo Editor Python')
        self.Centre()
        self.Show(True)

    def OnCombo(self, e):
        val = self.combo.GetValue()
        if val:
            out = self.originalImage.copy()
            out = out.filter(getattr(ImageFilter, val))
            self.UpdateImage(out)

    def OnMirror(self, e):
        out = self.filteredImage.transpose(Image.FLIP_LEFT_RIGHT)
        self.UpdateImage(out)

    def OnRotate90(self, e):
        out = self.filteredImage.rotate(90, expand=True)
        self.UpdateImage(out)

    def OnRotateDegrees(self, e):
        angle_str = self.rotate_degrees_text.GetValue()
        try:
            angle = int(angle_str)
            out = self.filteredImage.rotate(angle, expand=True, resample=Image.BICUBIC)
            self.UpdateImage(out)
        except ValueError:
            wx.MessageBox('Please enter a valid integer for rotation angle.', 'Error', wx.OK | wx.ICON_ERROR)

    def OnUndo(self, e):
        self.filteredImage = self.originalImage.copy()
        self.UpdateImage(self.filteredImage)

    def OnCrop(self, e):
        left = int(self.left_text.GetValue())
        upper = int(self.upper_text.GetValue())
        right = int(self.filteredImage.size[0])
        lower = int(self.filteredImage.size[1])
        out = self.filteredImage.crop((left, upper, right, lower))
        self.UpdateImage(out)

    def OnResize(self, e):
        new_width = int(self.width_text.GetValue())
        new_height = int(self.height_text.GetValue())
        out = self.filteredImage.resize((new_width, new_height))
        self.UpdateImage(out)

    def OnExportImage(self, e):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            self.filteredImage.save(filepath)
        dialog.Destroy()

    def UpdateImage(self, out):
        self.filteredImage = out
        self.image = wx.EmptyImage(out.size[0], out.size[1])
        self.image.SetData(out.convert("RGB").tobytes())
        self.image.SetAlpha(out.convert("RGBA").tobytes()[3::4])
        self.bitmap = wx.Bitmap(self.image)
        self.img.SetBitmap(self.bitmap)

if __name__ == '__main__':
    ex = wx.App()
    Example(None)
    ex.MainLoop()

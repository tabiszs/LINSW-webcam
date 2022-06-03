from urllib import parse
import tornado;
import tornado.web;
import tornado.ioloop;
import tornado.template;
import os;



class PhotoHandler(tornado.web.RequestHandler):
    def get(self):        
        try:       
            cam = self.application.settings['camera']
            cam.open()
            path2 = os.path.dirname(os.path.realpath(__file__)) + '/image'  
            filename = cam.save_image(path2);
            #self.write({f"{filename}"})
            self.write(filename)
            self.finish()
        except:
            self.redirect("/exception")
        finally:
            cam.release()
            return


class DownloadHandler(tornado.web.RequestHandler):
    def get(self):        
        try:       
            buf_size = 4096 
            filename=self.get_argument('filename', None)
            if not filename:
                self.write({"error":"File name is empty"})
                return
            self.set_header ('Content-Type','image/jpg')
            path2 = os.path.dirname(os.path.realpath(__file__)) + '/image'
            fn= f'{path2}/{filename}'
            with open( fn,'rb') as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    self.write(data)
            filename=parse.quote(filename)        
            self.set_header ('Content-Disposition','attachment; filename='+filename)
            self.finish()
        except:
            self.redirect("/download?invalidPath=true")
            return

# class DownloadHandler(tornado.web.RequestHandler):
#     def get(self):        
#         try:       
#             buf_size = 4096 
#             # make photo
#             cam = self.application.settings['camera']
#             cam.open()
#             path2 = os.path.dirname(os.path.realpath(__file__)) + '/image'
#             filename = cam.save_image(path2);
#             # send photo
#             self.set_header ('Content-Type','image/jpeg')
#             fn= f'{path2}/{filename}'
#             with open( fn,'rb') as f:
#                 while True:
#                     data = f.read(buf_size)
#                     if not data:
#                         break
#                     self.write(data)
#             filename=parse.quote(filename)        
#             self.set_header ('Content-Disposition','attachment; filename='+filename)
#             self.finish()
#         except:
#             self.redirect("/exception")
#         finally:
#             cam.release()
#             return
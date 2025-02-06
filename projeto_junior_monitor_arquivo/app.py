from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info('Informações sobre o processo.')
logging.warning('Aviso sobre algo que pode dar errado.')
logging.error('Erro ocorreu.')
logging.critical('Erro crítico.')
logging.debug('Esta é uma mensagem de debug.')

def minha_acao(event):
    logging.info(f'Arquivo detectado: {event.event_type} em {event.src_path}')

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        destino = '/home/yuri/projeto_junior_monitor_arquivo/enviar/' + event.src_path.split('/')[-1]
        shutil.move(event.src_path, destino)
        logging.info(f'Arquivo criado: {event.src_path}, enviado para {destino}')
        minha_acao(event)

        def on_modified(self, event):
            if event.is_directory:
                return
        destino = '/home/yuri/projeto_junior_monitor_arquivo/enviar/' + event.src_path.split('/')[-1]
        shutil.move(event.src_path, destino)
        logging.info(f'Arquivo modificado: {event.src_path}, enviado para {destino}')
        minha_acao(event)

observer = Observer()
observer.schedule(MyHandler(), path='/home/yuri/projeto_junior_monitor_arquivo/monitorado', recursive=False)

observer.start()

try:
    while True:
        time.sleep(1)  # Mantém o loop rodando para o observer
except KeyboardInterrupt:
    observer.stop()
observer.join()
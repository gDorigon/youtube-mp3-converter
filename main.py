import os
import threading
from tkinter import Tk, Label, Entry, filedialog, StringVar, messagebox, Frame, Listbox, END
from tkinter.ttk import Progressbar, Style, Button as TtkButton, Entry as TtkEntry, Label as TtkLabel
from pytube import YouTube

def download_audio_from_youtube(url, output_path, progress_var, progress_bar):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = os.path.join(output_path, yt.title + '.mp3')

        def progress_function(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = (bytes_downloaded / total_size) * 100
            progress_var.set(percentage_of_completion)
            progress_bar.update_idletasks()

        yt.register_on_progress_callback(progress_function)
        audio_stream.download(output_path, filename=yt.title + '.mp3')

        messagebox.showinfo("Concluído", f"Download completo! Arquivo salvo em: {output_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def browse_output_path():
    directory = filedialog.askdirectory()
    output_path_var.set(directory)

def add_to_queue():
    url = url_var.get()
    if url:
        queue_listbox.insert(END, url)
        url_var.set("")

def start_download_queue():
    output_path = output_path_var.get()
    if not output_path:
        messagebox.showwarning("Atenção", "Por favor, selecione o caminho para salvar os arquivos.")
        return

    def download_next():
        if queue_listbox.size() > 0:
            url = queue_listbox.get(0)
            queue_listbox.delete(0)
            progress_var.set(0)
            download_audio_from_youtube(url, output_path, progress_var, progress_bar)
            root.after(100, download_next)  # Call download_next after 100ms
        else:
            messagebox.showinfo("Concluído", "Todos os downloads foram concluídos.")

    threading.Thread(target=download_next).start()

# Configuração da janela principal
root = Tk()
root.title("Baixar Músicas do YouTube")
root.geometry("600x450")
root.configure(bg='#e0f7fa')  # Fundo levemente azul

# Aplicar o tema
style = Style()
style.theme_use('clam')

# Estilização
style.configure('TLabel', background='#e0f7fa', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12), padding=6, relief='raised', background='#00796b', foreground='white')
style.map('TButton', background=[('active', '#004d40')])
style.configure('TEntry', font=('Arial', 12), padding=5)
style.configure('TProgressbar', thickness=20)

# Variáveis
url_var = StringVar()
output_path_var = StringVar()
progress_var = StringVar()

# Widgets
TtkLabel(root, text="URL do Vídeo do YouTube:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
TtkEntry(root, textvariable=url_var, width=50).grid(row=0, column=1, padx=10, pady=5, sticky='ew')

TtkButton(root, text="Adicionar à Fila", command=add_to_queue).grid(row=0, column=2, padx=10, pady=5)

TtkLabel(root, text="Fila de Downloads:").grid(row=1, column=0, sticky='nw', padx=10, pady=5)
queue_listbox = Listbox(root, width=50, height=10, font=('Arial', 12), bg='#ffffff', borderwidth=0, highlightthickness=0)
queue_listbox.grid(row=1, column=1, padx=10, pady=5, sticky='nsew', columnspan=2)

TtkLabel(root, text="Caminho para salvar o arquivo:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
TtkEntry(root, textvariable=output_path_var, width=50).grid(row=2, column=1, padx=10, pady=5, sticky='ew', columnspan=2)

# Frame para conter os botões
button_frame = Frame(root, bg='#e0f7fa')
button_frame.grid(row=3, column=0, columnspan=3, pady=10)

TtkButton(button_frame, text="Procurar", command=browse_output_path).pack(side='left', padx=5)
TtkButton(button_frame, text="Baixar", command=start_download_queue).pack(side='left', padx=5)

progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var, style='TProgressbar')
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=20, sticky='ew')

# Configurar pesos das linhas e colunas
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# Inicia a interface gráfica
root.mainloop()

from shiny import App, ui, reactive, render
import functions as encrypt
import extract as decrypt
app_ui = ui.page_fluid(
    ui.panel_title("Image Watermark Encryption and Decryption"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h3("图像加密"),
            ui.input_file("upload_encrypt", "Upload an Image", multiple=False, accept=["image/*"]),
            ui.input_text("text", "Watermark Text", value="统计计算期末课程作业"),
            ui.input_action_button("submit_encrypt", "Encrypt Image"),
            ui.h3("图像解密"),
            ui.input_file("upload_decrypt", "Upload an Image", multiple=False, accept=["image/*"]),
            ui.input_numeric("wm_shape", "Watermark Shape(UTF-8编码下的字节数)", value=30, min=1),
            ui.input_action_button("submit_decrypt", "Decrypt Image")
        ),
        ui.panel_main(
            ui.h4("原始图片"),
            ui.output_image("original_img"),
            ui.h4("加密图片"),
            ui.output_image("encrypted_img"),
            ui.download_button("download_encrypted", "Download Encrypted Image"),
            ui.h4("解密内容"),
            ui.output_text("decrypted_text")
        )
    )
)

def server(input, output, session):
    @reactive.Calc
    def process_encryption():
        if input.upload_encrypt() and input.text():
            uploaded_file = input.upload_encrypt()[0]['datapath']
            watermark_text = input.text()
            a = encrypt.text_core_function(encoding='utf-8')
            a.init_emb_func(uploaded_file, watermark_text)
            encrypted_file_path = 'encrypted.png'
            a.embed(filename=encrypted_file_path)
            return {"original": uploaded_file, "encrypted": encrypted_file_path}
        return None

    @reactive.Calc
    def process_decryption():
        if input.upload_decrypt() and input.wm_shape():
            uploaded_file = input.upload_decrypt()[0]['datapath']
            wm_shape = input.wm_shape()
            a = decrypt.extractor(encoding='utf-8')
            decrypted_text = a.extract_form_file(filename=uploaded_file, wm_shape=wm_shape*8)
            return decrypted_text
        return ""

    @output
    @render.image
    def original_img():
        result = process_encryption()
        if result:
            return {"src": result["original"], "width": "20%", "height": "auto"}
        return None

    @output
    @render.image
    def encrypted_img():
        result = process_encryption()
        if result:
            return {"src": result["encrypted"], "width": "20%", "height": "auto"}
        return None

    @output
    @render.download
    def download_encrypted():
        result = process_encryption()
        if result:
            return result["encrypted"]
        return None

    @output
    @render.text
    def decrypted_text():
        return process_decryption()

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
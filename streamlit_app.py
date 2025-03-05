import streamlit as st
import numpy as np
import cv2
from PIL import Image

def extract_lsb(image):
    # Konversi gambar ke array numpy
    img_array = np.array(image)
    # Ambil bit LSB dari setiap piksel
    lsb_array = img_array & 1  # Operasi AND dengan 1 untuk mendapatkan bit terakhir
    return lsb_array

def detect_steganography(original, stego):
    # Konversi ke array numpy
    original_array = np.array(original)
    stego_array = np.array(stego)
    
    # Ambil bit LSB dari kedua gambar
    lsb_original = original_array & 1
    lsb_stego = stego_array & 1
    
    # Hitung perbedaan
    diff = np.sum(lsb_original != lsb_stego)
    
    return diff

def main():
    st.title("Deteksi Steganografi LSB")
    st.write("Unggah gambar untuk mendeteksi adanya steganografi menggunakan metode Least Significant Bit (LSB)")
    
    uploaded_file_original = st.file_uploader("Unggah Gambar Asli", type=["png", "jpg", "jpeg"])
    uploaded_file_stego = st.file_uploader("Unggah Gambar Steganografi", type=["png", "jpg", "jpeg"])
    
    if uploaded_file_original and uploaded_file_stego:
        original = Image.open(uploaded_file_original).convert("RGB")
        stego = Image.open(uploaded_file_stego).convert("RGB")
        
        st.image([original, stego], caption=["Gambar Asli", "Gambar Steganografi"], width=300)
        
        # Deteksi perbedaan LSB
        diff = detect_steganography(original, stego)
        
        if diff > 0:
            st.error(f"Deteksi steganografi: Ditemukan perubahan pada {diff} piksel!")
        else:
            st.success("Tidak ditemukan indikasi steganografi.")
        
        # Tampilkan bit LSB
        st.subheader("Ekstraksi Bit LSB")
        lsb_stego = extract_lsb(stego)
        st.image(lsb_stego * 255, caption="Ekstraksi LSB dari Gambar Steganografi", width=300)

if __name__ == "__main__":
    main()

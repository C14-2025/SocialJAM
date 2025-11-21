const UploadImage = ({ selectedImages = [], setSelectedImages }) => {
  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    if (files.length > 0) {
      setSelectedImages([...selectedImages, ...files]);
    }
  };

  const removeImage = (index) => {
    const newImages = selectedImages.filter((_, i) => i !== index);
    setSelectedImages(newImages);
  };

  // Return the JSX for rendering
  return (
    <div className="file_uploader-box flex flex-col items-center gap-2 ">
      {selectedImages.length > 0 && (
        <div className="w-full grid grid-cols-2 gap-4">
          {selectedImages.map((image, index) => (
            <div key={index} className="relative">
              <img
                alt={`Preview ${index + 1}`}
                className="file_uploader-img w-full h-48 object-cover rounded-xl"
                src={URL.createObjectURL(image)}
              />
              <button
                type="button"
                onClick={() => removeImage(index)}
                className="absolute top-2 right-2 bg-dark-4 hover:bg-red-600 text-white rounded-full p-2 transition"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="flex flex-col items-center justify-center w-full h-full mt-4">
        <label
          className="cursor-pointer flex flex-col items-center gap-4"
          htmlFor="file-upload"
        >
          <img
            src="/assets/icons/file-upload.svg"
            alt="upload"
            width={96}
            height={96}
          />

          <div className="shad-button_dark_4 rounded-xl py-3">
            {selectedImages.length > 0
              ? "Adicionar mais imagens"
              : "Escolher imagem"}
          </div>
        </label>
        <input
          id="file-upload"
          type="file"
          name="myImage"
          accept="image/*"
          multiple
          style={{ display: "none" }}
          onChange={handleImageChange}
        />
      </div>
    </div>
  );
};

export default UploadImage;

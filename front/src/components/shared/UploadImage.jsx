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
    <div className="flex flex-col bg-dark-3 rounded-xl border border-dark-4 p-5 h-auto min-h-[200px]">
      {selectedImages.length > 0 && (
        <div className="w-full grid grid-cols-2 gap-3 mb-4">
          {selectedImages.map((image, index) => (
            <div key={index} className="relative">
              <img
                alt={`Preview ${index + 1}`}
                className="w-full h-40 object-cover rounded-xl"
                src={URL.createObjectURL(image)}
              />
              <button
                type="button"
                onClick={() => removeImage(index)}
                className="absolute top-2 right-2 bg-dark-4 hover:bg-red-600 text-white rounded-full w-7 h-7 flex items-center justify-center transition text-sm"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      <label
        className="cursor-pointer flex flex-col items-center justify-center gap-3 w-full py-6 hover:opacity-80 transition"
        htmlFor="file-upload"
      >
        <img
          src="/assets/icons/file-upload.svg"
          alt="upload"
          width={80}
          height={80}
        />

        <p className="text-light-4 small-regular text-center">
          {selectedImages.length > 0
            ? "Adicionar mais imagens"
            : "Clique para selecionar"}
        </p>
        
        <input
          id="file-upload"
          type="file"
          name="myImage"
          accept="image/*"
          multiple
          style={{ display: "none" }}
          onChange={handleImageChange}
        />
      </label>
    </div>
  );
};

export default UploadImage;

import { useState } from "react";

const UploadImage = () => {
  // Define a state variable to store the selected image
  const [selectedImage, setSelectedImage] = useState(null);

  // Return the JSX for rendering
  return (
        <div className="file_uploader-box flex flex-col items-center gap-2 ">

            {selectedImage && (
                <div className="cursor-pointer" >
                {/* Display the selected image */}
                <img
                    alt="not found"
                    className="file_uploader-img"
                    src={URL.createObjectURL(selectedImage)}
                />
                {/* Button to remove the selected image */}
                <button onClick={() => setSelectedImage(null)} className="shad-button_dark_4 rounded-xl py-3 justify-center w-full h-full">

                    Remover

                </button>
                </div>
            )}

            {!selectedImage && (
                <div className="flex flex-col items-center justify-center w-full h-full">
                    <label className="cursor-pointer flex flex-col items-center gap-4" htmlFor="file-upload">
                        <img
                            src="/assets/icons/file-upload.svg"
                            alt="upload"
                            width={96}
                            height={96}
                        />

                        <div className="shad-button_dark_4 rounded-xl py-3">
                            {selectedImage ? "Alterar imagem" : "Escolher imagem"}
                        </div>

                    </label>
                    <input
                        id="file-upload"
                        type="file"
                        name="myImage"
                        accept="image/*"
                        style={{ display: "none" }}
                        onChange={(event) => {
                        // Update the state with the selected image file
                            console.log(event.target.files[0]);
                            setSelectedImage(event.target.files[0]);
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default UploadImage;
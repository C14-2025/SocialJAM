export default function CardUser({image, nomeUsuario, artistaFav}) {
    return (
        <div className="flex flex-col justify-center items-center h-screen mx-auto text-center">
            
            
            <div className="mb-8">
                {image ? (
                    <img 
                        src={image} 
                        alt="Foto de perfil"
                        className="h-[300px] w-[300px] rounded-full object-cover border-4 border-primary-500 shadow-2xl"
                    />
                ) : (
                    <img 
                        src='/assets/icons/profile-placeholder.svg' 
                        alt="Foto de perfil padrão"
                        className="h-[300px] w-[300px] rounded-full object-cover border-4 border-gray-600 shadow-2xl bg-gray-800 p-8"
                    />
                )}
            </div>

           
            <div className="space-y-4">
                <h1 className="text-4xl font-bold text-white mb-2 tracking-wide">
                    {nomeUsuario}
                </h1>
                
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl px-6 py-4 border border-gray-700">
                    <h5 className="text-lg text-gray-300">
                        <span className="text-primary-500 font-semibold">Artista favorito:</span>
                        <br />
                        <span className="text-white font-medium">{artistaFav}</span>
                    </h5>
                </div>
            </div>
        </div>
    );
}
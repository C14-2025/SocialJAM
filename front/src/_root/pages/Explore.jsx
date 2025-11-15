import React, { useState, useEffect } from 'react';
import { getAllArtists } from '@/api';
import { use } from 'react';
import { useNavigate } from 'react-router-dom';

const Explore = () => {
  //provisório, só até a implementação do spotify api
  const [artists, setArtists] = useState([
    {
      id: 1,
      name: 'Milton Nascimento',
      followers: 1500000,
      genres: ['MPB', 'Jazz', 'Bossa Nova'],
      popularity: 75
    },
    {
      id: 2,
      name: 'Geordie Greep',
      followers: 250000,
      genres: ['Math Rock', 'Progressive Rock', 'Experimental'],
      popularity: 68
    },
    {
      id: 3,
      name: 'Fiona apple',
      followers: 2100000,
      genres: ['MPB', 'Samba', 'Bossa Nova'],
      popularity: 82
    },
    {
      id: 4,
      name: 'King Crimson',
      followers: 1800000,
      genres: ['Progressive Rock', 'Art Rock'],
      popularity: 70
    },
    {
      id: 5,
      name: 'Chico Buarque',
      followers: 1900000,
      genres: ['MPB', 'Samba', 'Bossa Nova'],
      popularity: 78
    },
    {
      id: 6,
      name: 'black midi',
      followers: 320000,
      genres: ['Experimental Rock', 'Math Rock', 'Noise Rock'],
      popularity: 65
    },
    {
      id: 7,
      name: 'bitols',
      followers: 8500000,
      genres: ['Alternative Rock', 'Art Rock', 'Electronic'],
      popularity: 88
    }
  ]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArtists = async () => {
      setLoading(true);
      const result = await getAllArtists();
      if (result.success && result.artists.length > 0) {
        setArtists(result.artists);
      }
      setLoading(false);
    };
    
    // pra usar a api de vdd tem que descomentar
    // fetchArtists();
  }, []);

  const handleArtistClick = (artistId) => {
    navigate(`/artist/${artistId}`);
  }

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-light-3">Carregando artistas...</p>
      </div>
    );
  }
  //imagens para ficarem passando no fundo qualquer coisa deem sugestoes no grupo ou coloquem aqui
  const backgrounds = [
  "/assets/images/fredao_2.jpg",
  "/assets/images/davemusta.png",
  "/assets/images/kendrick.png",
  "/assets/images/rihanna.png",
  ];

  const [bgIndex, setBgIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
    setBgIndex((prev) => (prev + 1) % backgrounds.length);
    }, 10000); // troca a imagem a cada 10 segundos se quiserem podem mudar o tempo

    return () => clearInterval(interval);
  }, []);


  return (
    <div className="flex flex-1 min-h-screen bg-slideshow"
    style={{
    backgroundImage: `url(${backgrounds[bgIndex]})`,
    }}>
      <div className="common-container bg-black/40 backdrop-blur-sm rounded-xl p-6">
        <h1 className="h3-bold md:h2-bold text-left w-full mb-8">Explorar Artistas</h1>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-7">
          {artists.map((artist) => (
            <div 
              key={artist.id} 
              className="bg-dark-3 rounded-2xl cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl p-4"
              onClick={() => handleArtistClick(artist.id)}
            >
              <img 
                src={artist.photo || '/assets/icons/profile-placeholder.svg'} 
                alt={artist.name}
                className="w-full h-48 object-cover rounded-xl"
              />
              <div className="p-2">
                <p className="base-medium text-light-1 line-clamp-1 mb-2">
                  {artist.name}
                </p>
                <p className="small-regular text-light-3">
                  {artist.followers} seguidores
                </p>
                {artist.genres && artist.genres.length > 0 && (
                  <p className="tiny-medium text-light-3 mt-2">
                    {artist.genres.slice(0, 2).join(', ')}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-2">
                  <span className="tiny-medium text-light-3">
                    Popularidade: {artist.popularity}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Explore;
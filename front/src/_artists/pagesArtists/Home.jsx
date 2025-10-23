import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const Home = () => {
  const { artistId } = useParams();
  const [artist, setArtist] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArtistData = async () => {
      setLoading(true);

      // simula dados
      const artistsData = {
        1: {
          id: "1",
          name: "Milton Nascimento",
          followers: 1500000,
          genres: ["MPB", "Jazz", "Bossa Nova"],
          popularity: 85,
          photo: "/assets/icons/profile-placeholder.svg",
          bio: "Cantor e compositor brasileiro, um dos maiores nomes da MPB. Sua voz única e suas composições marcaram gerações.",
        },
        2: {
          id: "2",
          name: "Geordie Greep",
          followers: 250000,
          genres: ["Math Rock", "Progressive Rock", "Experimental"],
          popularity: 68,
          photo: "/assets/icons/profile-placeholder.svg",
          bio: "Random que tocava umas musicas ai",
        },
        3: {
          id: "3",
          name: "Fiona apple",
          followers: 2100000,
          genres: ["MPB", "Samba", "Bossa Nova"],
          popularity: 82,
          photo: "/assets/icons/profile-placeholder.svg",
          bio: "Random 2 que tocava umas musicas ai",
        },
        4: {
          id: "4",
          name: "King Crimson",
          followers: 1800000,
          genres: ["Progressive Rock", "Art Rock"],
          popularity: 70,
          photo: "/assets/icons/profile-placeholder.svg",
          bio: "Uma das bandas mais influentes do rock progressivo, conhecida por suas composições complexas e experimentais.",
        },
      };

      const mockPosts = [
        {
          id: 1,
          author: "João Silva",
          authorPhoto: "/assets/icons/profile-placeholder.svg",
          content:
            'Acabei de ouvir "Clube da Esquina" e estou sem palavras! 🎵 Uma obra-prima atemporal.',
          likes: 45,
          comments: 12,
          createdAt: "2h atrás",
          liked: false,
        },
        {
          id: 2,
          author: "Maria Santos",
          authorPhoto: "/assets/icons/profile-placeholder.svg",
          content:
            'A voz desse artista é simplesmente celestial. "Travessia" é minha música favorita!',
          likes: 78,
          comments: 23,
          createdAt: "5h atrás",
          liked: true,
        },
        {
          id: 3,
          author: "Pedro Costa",
          authorPhoto: "/assets/icons/profile-placeholder.svg",
          content:
            "Fui no show ontem e foi incrível! A energia é contagiante! 🔥",
          likes: 120,
          comments: 34,
          createdAt: "1 dia atrás",
          liked: false,
        },
      ];

      setArtist(artistsData[artistId] || null);
      setPosts(mockPosts);
      setLoading(false);

      // api real, descomentar
      // const artistData = await getArtistById(artistId);
      // const artistPosts = await getPostsByArtist(artistId);
    };

    fetchArtistData();
  }, [artistId]);

  if (loading) {
    return (
      <div className="flex-center w-full h-screen">
        <div className="flex-center gap-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
          <p className="text-light-3">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!artist) {
    return (
      <div className="flex-center w-full h-screen">
        <div className="flex-center flex-col gap-4">
          <img
            src="/assets/icons/wallpaper.svg"
            alt="Not found"
            className="w-20 h-20 opacity-50"
          />
          <p className="text-light-3">Artista não encontrado</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-1">
      <div className="home-container">
        <div className="max-w-screen-sm w-full">
          {/* Header do Artista */}
          <div className="bg-dark-2 rounded-3xl border border-dark-4 p-6 mb-8">
            <div className="flex items-start gap-6">
              <img
                src={artist.photo}
                alt={artist.name}
                className="w-32 h-32 rounded-full object-cover border-4 border-primary-500 shadow-lg"
              />
              <div className="flex-1">
                <h1 className="h2-bold text-light-1 mb-2">{artist.name}</h1>
                <p className="small-regular text-light-3 mb-4">
                  {artist.followers?.toLocaleString()} seguidores
                </p>
                {artist.genres && artist.genres.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {artist.genres.map((genre, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-dark-4 rounded-full text-light-3 tiny-medium"
                      >
                        {genre}
                      </span>
                    ))}
                  </div>
                )}
                <p className="base-regular text-light-2">{artist.bio}</p>
              </div>
            </div>
          </div>

          {/* Feed de Posts */}
          <div className="home-posts">
            <h2 className="h3-bold text-light-1 mb-6">
              Posts sobre {artist.name}
            </h2>

            {posts.length === 0 ? (
              <div className="flex-center w-full h-40 bg-dark-2 rounded-3xl border border-dark-4">
                <p className="text-light-3">
                  Nenhum post ainda. Seja o primeiro a postar sobre{" "}
                  {artist.name}!
                </p>
              </div>
            ) : (
              posts.map((post) => (
                <div key={post.id} className="post-card">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <img
                        src={post.authorPhoto}
                        alt={post.author}
                        className="w-10 h-10 rounded-full"
                      />
                      <div>
                        <p className="base-medium text-light-1">
                          {post.author}
                        </p>
                        <p className="tiny-medium text-light-3">
                          {post.createdAt}
                        </p>
                      </div>
                    </div>
                  </div>

                  <p className="base-regular text-light-2 mb-5">
                    {post.content}
                  </p>

                  <div className="flex items-center gap-6 text-light-3">
                    <button className="flex items-center gap-2 hover:text-primary-500 transition">
                      <img
                        src={
                          post.liked
                            ? "/assets/icons/liked.svg"
                            : "/assets/icons/like.svg"
                        }
                        alt="Curtir"
                        className="w-5 h-5"
                      />
                      <span className="small-medium">{post.likes}</span>
                    </button>
                    <button className="flex items-center gap-2 hover:text-primary-500 transition">
                      <img
                        src="/assets/icons/chat.svg"
                        alt="Comentar"
                        className="w-5 h-5"
                      />
                      <span className="small-medium">{post.comments}</span>
                    </button>
                    <button className="flex items-center gap-2 hover:text-primary-500 transition ml-auto">
                      <img
                        src="/assets/icons/bookmark.svg"
                        alt="Salvar"
                        className="w-5 h-5"
                      />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

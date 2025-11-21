import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getSpotifyArtistById, getPostsByArtist } from "../../api";

const Home = () => {
  const { artistId } = useParams();
  const [artist, setArtist] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArtistData = async () => {
      setLoading(true);
      setError(null);

      try {
        // Buscar dados do artista da API do Spotify
        const artistResult = await getSpotifyArtistById(artistId);

        if (artistResult.success) {
          setArtist(artistResult.artist);
        } else {
          setError(artistResult.error);
          setArtist(null);
        }

        // Buscar posts do artista
        const postsResult = await getPostsByArtist(artistId);
        if (postsResult.success) {
          console.log("Posts recebidos:", postsResult.posts);
          console.log("Primeiro post:", postsResult.posts[0]);
          setPosts(postsResult.posts);
        } else {
          console.error("Erro ao buscar posts:", postsResult.error);
          setPosts([]);
        }
      } catch (err) {
        console.error("Erro ao buscar dados do artista:", err);
        setError("Erro ao carregar dados do artista");
        setArtist(null);
      } finally {
        setLoading(false);
      }
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
          <p className="text-light-3">{error || "Artista não encontrado"}</p>
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
                src={artist.photo || "/assets/icons/profile-placeholder.svg"}
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
                {artist.popularity !== undefined && (
                  <div className="flex items-center gap-2">
                    <span className="text-light-3 small-regular">
                      Popularidade:
                    </span>
                    <div className="flex-1 max-w-xs bg-dark-4 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full"
                        style={{ width: `${artist.popularity}%` }}
                      />
                    </div>
                    <span className="text-light-2 small-medium">
                      {artist.popularity}%
                    </span>
                  </div>
                )}
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
                <div key={post._id || post.id} className="post-card">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <img
                        src={
                          post.author?.user_photo_url
                            ? `http://localhost:8000/${post.author.user_photo_url}`
                            : "/assets/icons/profile-placeholder.svg"
                        }
                        alt={post.author?.name || "User"}
                        className="w-10 h-10 rounded-full object-cover"
                      />
                      <div>
                        <p className="base-medium text-light-1">
                          {post.author?.name}
                        </p>
                        <p className="tiny-medium text-light-3">
                          {new Date(post.created_at).toLocaleDateString(
                            "pt-BR"
                          )}
                        </p>
                      </div>
                    </div>
                  </div>

                  <p className="base-regular text-light-2 mb-5">
                    {post.content}
                  </p>

                  {/* Mostrar imagens se existirem */}
                  {post.images && post.images.length > 0 && (
                    <div
                      className={`grid gap-2 mb-5 ${
                        post.images.length === 1
                          ? "grid-cols-1"
                          : post.images.length === 2
                          ? "grid-cols-2"
                          : "grid-cols-2"
                      }`}
                    >
                      {post.images.map((image, index) => (
                        <img
                          key={index}
                          src={`http://localhost:8000/${image}`}
                          alt={`Post image ${index + 1}`}
                          className="w-full h-auto rounded-xl object-cover max-h-96"
                        />
                      ))}
                    </div>
                  )}

                  <div className="flex items-center gap-6 text-light-3">
                    <button className="flex items-center gap-2 hover:text-primary-500 transition">
                      <img
                        src={
                          post.liked_by && post.liked_by.length > 0
                            ? "/assets/icons/liked.svg"
                            : "/assets/icons/like.svg"
                        }
                        alt="Curtir"
                        className="w-5 h-5"
                      />
                      <span className="small-medium">{post.likes || 0}</span>
                    </button>
                    <button className="flex items-center gap-2 hover:text-primary-500 transition">
                      <img
                        src="/assets/icons/chat.svg"
                        alt="Comentar"
                        className="w-5 h-5"
                      />
                      <span className="small-medium">0</span>
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

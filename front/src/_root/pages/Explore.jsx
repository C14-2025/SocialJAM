import { useState, useEffect, useCallback, useRef } from "react";
import {
  getSpotifyTopArtists,
  hasSpotifyConnected,
  searchSpotifyArtists,
} from "@/api";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { InputGroup, InputGroupInput } from "@/components/ui/input-group";

const LOCAL_STORAGE_KEY = "spotify_top_artists";
const BACKGROUND_IMAGES = [
  "/assets/images/fredao_2.jpg",
  "/assets/images/davemusta.png",
  "/assets/images/kendrick.png",
  "/assets/images/rihanna.png",
];

const DEFAULT_ARTISTS = [
  {
    id: 1,
    name: "Milton Nascimento",
    followers: 1500000,
    genres: ["MPB", "Jazz", "Bossa Nova"],
    popularity: 75,
  },
  {
    id: 2,
    name: "Geordie Greep",
    followers: 250000,
    genres: ["Math Rock", "Progressive Rock", "Experimental"],
    popularity: 68,
  },
  {
    id: 3,
    name: "Fiona apple",
    followers: 2100000,
    genres: ["MPB", "Samba", "Bossa Nova"],
    popularity: 82,
  },
  {
    id: 4,
    name: "King Crimson",
    followers: 1800000,
    genres: ["Progressive Rock", "Art Rock"],
    popularity: 70,
  },
  {
    id: 5,
    name: "Chico Buarque",
    followers: 1900000,
    genres: ["MPB", "Samba", "Bossa Nova"],
    popularity: 78,
  },
  {
    id: 6,
    name: "black midi",
    followers: 320000,
    genres: ["Experimental Rock", "Math Rock", "Noise Rock"],
    popularity: 65,
  },
  {
    id: 7,
    name: "bitols",
    followers: 8500000,
    genres: ["Alternative Rock", "Art Rock", "Electronic"],
    popularity: 88,
  },
];

const Explore = () => {
  const [artists, setArtists] = useState(DEFAULT_ARTISTS);
  const [topArtists, setTopArtists] = useState(DEFAULT_ARTISTS);
  const [loadingSpotify, setLoadingSpotify] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const { user, isLoading: authLoading } = useAuth();
  const navigate = useNavigate();
  const hasAutoFetched = useRef(false);
  const [bgIndex, setBgIndex] = useState(0);

  useEffect(() => {
    try {
      const cachedArtists = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (cachedArtists) {
        const parsedArtists = JSON.parse(cachedArtists);
        if (Array.isArray(parsedArtists) && parsedArtists.length > 0) {
          setTopArtists(parsedArtists);
          setArtists(parsedArtists);
        }
      }
    } catch (error) {
      console.error("Erro ao carregar artistas salvos localmente:", error);
    }
  }, []);

  const handleFetchSpotifyTopArtists = useCallback(
    async ({ showAlerts = true } = {}) => {
      setLoadingSpotify(true);
      try {
        const result = await getSpotifyTopArtists();
        if (result.success && result.artists) {
          setTopArtists(result.artists);
          setArtists(result.artists);
          localStorage.setItem(
            LOCAL_STORAGE_KEY,
            JSON.stringify(result.artists)
          );
          setSearchValue((prev) => (prev ? "" : prev));
          if (showAlerts) {
            alert(
              `✅ ${result.artists.length} artistas carregados do Spotify!`
            );
          }
        } else if (result.needsAuth) {
          if (showAlerts) {
            alert(
              "⚠️ Você precisa conectar sua conta Spotify primeiro! Vá até o Profile."
            );
          }
        } else {
          if (showAlerts) {
            alert("❌ Erro ao buscar artistas: " + result.error);
          }
        }
      } catch {
        if (showAlerts) {
          alert("❌ Erro ao buscar artistas do Spotify");
        }
      } finally {
        setLoadingSpotify(false);
      }
    },
    []
  );

  useEffect(() => {
    if (authLoading || hasAutoFetched.current) {
      return;
    }

    hasAutoFetched.current = true;

    if (user && hasSpotifyConnected(user)) {
      handleFetchSpotifyTopArtists({ showAlerts: false });
    }
  }, [authLoading, user, handleFetchSpotifyTopArtists]);

  useEffect(() => {
    const trimmedValue = searchValue.trim();

    if (!trimmedValue) {
      setSearchLoading(false);
      setArtists(
        topArtists && topArtists.length > 0 ? topArtists : DEFAULT_ARTISTS
      );
      return;
    }

    let isActive = true;
    setSearchLoading(true);

    const handler = setTimeout(async () => {
      try {
        const result = await searchSpotifyArtists(trimmedValue);
        if (!isActive) {
          return;
        }

        if (result.success && Array.isArray(result.artists)) {
          setArtists(result.artists);
        } else if (result.needsAuth) {
          alert(
            "⚠️ Você precisa conectar sua conta Spotify primeiro! Vá até o Profile."
          );
          setArtists(
            topArtists && topArtists.length > 0 ? topArtists : DEFAULT_ARTISTS
          );
        } else {
          alert("❌ Erro ao buscar artistas: " + result.error);
          setArtists(
            topArtists && topArtists.length > 0 ? topArtists : DEFAULT_ARTISTS
          );
        }
      } catch (error) {
        if (!isActive) {
          return;
        }
        alert("❌ Erro inesperado ao buscar artistas no Spotify");
        setArtists(
          topArtists && topArtists.length > 0 ? topArtists : DEFAULT_ARTISTS
        );
        console.error("Erro inesperado ao buscar artistas no Spotify:", error);
      } finally {
        if (isActive) {
          setSearchLoading(false);
        }
      }
    }, 400);

    return () => {
      isActive = false;
      clearTimeout(handler);
    };
  }, [searchValue, topArtists]);

  const handleArtistClick = (artistId) => {
    navigate(`/artist/${artistId}`);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setBgIndex((prev) => (prev + 1) % BACKGROUND_IMAGES.length);
    }, 10000); // troca a imagem a cada 10 segundos se quiserem podem mudar o tempo

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className="flex flex-1 min-h-screen bg-slideshow"
      style={{
        backgroundImage: `url(${BACKGROUND_IMAGES[bgIndex]})`,
      }}
    >
      <div className="common-container bg-black/40 backdrop-blur-sm rounded-xl p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <h1 className="h3-bold md:h2-bold text-left">Explorar Artistas</h1>
          <Button
            onClick={() => handleFetchSpotifyTopArtists()}
            disabled={loadingSpotify || searchLoading}
            className="bg-green-600 hover:bg-green-700"
          >
            {loadingSpotify ? "⏳ Carregando..." : "🎵 Buscar Meus Top Artists"}
          </Button>
        </div>
        <InputGroup className="w-full max-w-5xl bg-dark-4 rounded-xl border-2 border-transparent focus-within:border-white transition-colors">
          <InputGroupInput
            placeholder="Busque artistas"
            className="h-12 bg-transparent border-none placeholder:text-light-4 focus-visible:ring-0 focus-visible:ring-offset-0 text-light-1"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
          />
        </InputGroup>

        {searchLoading && (
          <p className="text-light-3 mt-2">Buscando artistas no Spotify...</p>
        )}
        {!searchLoading && searchValue.trim() && artists.length === 0 && (
          <p className="text-light-3 mt-2">
            Nenhum artista encontrado para &quot;{searchValue.trim()}&quot;.
          </p>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-7">
          {artists.map((artist) => (
            <div
              key={artist.id}
              className="bg-dark-3 rounded-2xl cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl p-4"
              onClick={() => handleArtistClick(artist.id)}
            >
              <img
                src={artist.photo || "/assets/icons/profile-placeholder.svg"}
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
                    {artist.genres.slice(0, 2).join(", ")}
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

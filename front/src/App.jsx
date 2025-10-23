import { Routes, Route, Navigate } from "react-router-dom";

import "./globals.css";
import SigninForms from "./_auth/forms/SigninForms";
import { Explore, Saved, AllUsers, Profile, UpdateProfile } from "./_root/pages";
import { Home, CreatePost, EditPost, PostDetails, LikedPosts } from "./_artists/pagesArtists";
import SignupForms from "./_auth/forms/SignupForms";
import AuthLayout from "./_auth/AuthLayout";
import RootLayout from "./_root/RootLayout";
import ProtectedRoute from "./components/shared/ProtectedRoute";
import { useAuth } from "./context/AuthContext";
import ArtistLayout from "./_artists/ArtistLayout";

const App = () => {
  const { user } = useAuth();

  return (
    <main className="flex h-screen">
      <Routes>
        {/* Rotas públicas */}
        <Route element={<AuthLayout />}>
          <Route path="/signup" element={<SignupForms />} />
          <Route path="/sign-in" element={<SigninForms />} />
        </Route>

        {/* Rotas privadas */}
        <Route
          element={
            <ProtectedRoute>
              <RootLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/explore" replace />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/saved" element={<Saved />} />
          <Route path="/all-users" element={<AllUsers />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/profile/:username" element={<Profile />} />
          <Route path="/update-profile/:id" element={<UpdateProfile />} />
        </Route>

        {/* Rotas privadas para artistas */}
        <Route
          element={
            <ProtectedRoute>
              <ArtistLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/artist/:artistId" element={<Home />} />
          <Route path="/artist/:artistId/create-post" element={<CreatePost />}/>
          <Route path="/update-post/:id" element={<EditPost />} />
          <Route path="/artist/:artistId/posts/:postId" element={<PostDetails />} />
          <Route path="/artist/:artistId/liked-posts" element={<LikedPosts />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate  to="/explore" replace />} />

      </Routes>
    </main>
  );
};

export default App;

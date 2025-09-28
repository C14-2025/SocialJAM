import {Routes, Route} from "react-router-dom"

import './globals.css';
import SigninForms from "./_auth/forms/SigninForms";
import {Explore, Home, Saved} from "./_root/pages";
import SignupForms from "./_auth/forms/SignupForms";
import AuthLayout from "./_auth/AuthLayout";
import RootLayout from "./_root/RootLayout";
import ProtectedRoute from "./components/shared/ProtectedRoute";
import AllUsers from "./_root/pages/AllUsers";
import CreatePost from "./_root/pages/CreatePost";
import EditPost from "./_root/pages/EditPost";
import PostDetails from "./_root/pages/PostDetails";
import Profile from "./_root/pages/Profile";
import UpdateProfile from "./_root/pages/UpdateProfile";



const App = () => {
  return (
    <main className="flex h-screen">
      <Routes>
        {/* Rotas públicas */}
        <Route element={<AuthLayout />}>
          <Route path="/signup" element={<SignupForms />} />
          <Route path="/sign-in" element={<SigninForms />} />
        </Route>

        {/* Rotas privadas */}
        <Route element={
          <ProtectedRoute>
            <RootLayout />
          </ProtectedRoute>
        }>
          <Route index element={<Home />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/saved" element={<Saved />} />
          <Route path="/all-users" element={<AllUsers />} />
          <Route path="/create-post" element={<CreatePost />} />
          <Route path="/update-post/:id" element={<EditPost />} />
          <Route path="/post/:id" element={<PostDetails />} />
          <Route path="/profile/:id/*" element={<Profile />} />
          <Route path="/update-profile/:id" element={<UpdateProfile />} />
        </Route>

      </Routes>
    </main>
  )
}

export default App
import { Link } from "react-router-dom";
import { useAuth } from '@/context/AuthContext';
import { Button } from "../ui/button";

const TopBar = () => {

    const { logout } = useAuth();
  
    const handleLogout = () => {
      logout();
    };
  return (
    <section className="topbar"
      
    >
      <div className="flex-between py-4 px-5">
        <Link to="/" className="flex gap-3 items-center">
          <img
            src="/assets/images/logo.svg"
            alt="logo"
            width={130}
            height={325}
          />
        </Link>

        <div className="flex gap-4">
          <Button variant="ghost" className="shad-button_ghost"
            onClick={handleLogout}>
              <img src="/assets/icons/logout.svg" alt="Logout" />
            
          </Button>

          <Link to="/profile" className="flex-center gap-3">

            {/* precisamos fazer a imagem ser dinâmica de acordo com o usuário !!!!*/}
            <img
              src="/assets/images/profile.png"
              alt="Profile"
              className="h-8 w-8 rounded-full"
            />

          </Link>
        </div>

      </div>

    </section>
  );
};

export default TopBar;

import { sidebarLinks } from "@/constants";
import { Link, NavLink, useLocation } from "react-router-dom";
import { Button } from "../ui/button";
import { useAuth } from "@/context/AuthContext";

const Leftsidebar = () => {
  const { pathname } = useLocation();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav
      className="leftsidebar"
      style={{
        flexDirection: "column",
        background: "#1f1f23",
        minWidth: "270px",
        padding: "40px 24px",
      }}
    >
      <div className="flex flex-col gap-11">
        <Link to="/" className="flex gap-3 items-center">
          <img
            src="/assets/images/Logo_SJ.svg"
            alt="logo"
            width={230}
            height={20}
          />
        </Link>

        {/* precisamos fazer a imagem e o nome serem dinâmicos de acordo com o usuário !!!!*/}
        <Link to={"/profile"} className="flex gap-3 items-center">
          <img
            src="/assets/images/profile.png"
            alt="profile"
            width={24}
            height={24}
            className="h-14 w-14 rounded-full"
          />

          <div className="flex flex-col">
            <p className="body-bold">Nome do Usuário</p>
            <p className="small-regular text-gray-3">@nomeusuario</p>
          </div>
        </Link>

        <ul className="flex flex-col gap-6">
          {sidebarLinks.map((link) => {
            const isActive = pathname === link.route;
            return (
              <li
                key={link.label}
                className={`leftsidebar-link group ${
                  isActive && "bg-primary-500"
                }`}
              >
                <NavLink
                  to={link.route}
                  className="flex gap-4 items-center p-4"
                >
                  <img
                    src={link.imgURL}
                    alt={link.label}
                    className={`group-hover:invert-white ${
                      isActive && "invert-white"
                    }`}
                  />
                  {link.label}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </div>

      <Button
        variant="ghost"
        className="shad-button_ghost"
        onClick={handleLogout}
      >
        <img src="/assets/icons/logout.svg" alt="Logout" />
        Sair
      </Button>
    </nav>
  );
};

export default Leftsidebar;

import React from "react";
import { useParams, NavLink, useLocation, Link } from "react-router-dom";
import { artistFeedTabs } from "@/constants";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";

const ArtistLeftSideBar = () => {
  const { pathname } = useLocation();
  const { logout, user } = useAuth();
  const { artistId } = useParams();

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
        <Link to="/explore" className="flex gap-3 items-center">
          <img
            src="/assets/images/Logo_SJ.svg"
            alt="logo"
            width={230}
            height={20}
          />
        </Link>

        <Link to={"profile"} className="flex gap-3 items-center">
          <img
            src="/assets/icons/profile-placeholder.svg"
            alt="profile"
            width={24}
            height={24}
            className="h-14 w-14 rounded-full"
          />

          <div className="flex flex-col">
            <p className="body-bold">{user?.nome || ""}</p>
          </div>
        </Link>


        <ul className="flex flex-col gap-6">
          {artistFeedTabs.map((link) => {
            const fullRoute = link.route 
              ? `/artist/${artistId}/${link.route}` 
              : `/artist/${artistId}`;
            
            const isActive = pathname === fullRoute;
            
            return (
              <li
                key={link.label}
                className={`leftsidebar-link group ${isActive && "bg-primary-500"}`}
              >
                <NavLink 
                  to={fullRoute} 
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

export default ArtistLeftSideBar;
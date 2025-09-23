import { sidebarLinks } from "@/constants";
import { Link, NavLink } from "react-router-dom";

const Leftsidebar = () => {
  return (
    <nav
      className="leftsidebar"
      style={{
        display: "flex",
        flexDirection: "column",
        background: "#1f1f23",
        minWidth: "270px",
        padding: "40px 24px",
      }}
    >
      <div className="flex flex-col gap-11">
        <Link to="/" className="flex gap-3 items-center">
          <img
            src="/assets/images/logo.svg"
            alt="logo"
            width={170}
            height={36}
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
            return (

              <li key={link.label}
              className = "leftsidebar_link">

                <NavLink 
                  to={link.route}
                  className="flex gap-4 items-center p-4"
                >
                  <img
                    src={link.imgURL}
                    alt={link.label}
                    className="group-hover:invert-white"
                  />
                  {link.label}
 
                </NavLink>
              </li>
            )
          })}

        </ul>
      </div>
    </nav>
  );
};

export default Leftsidebar;

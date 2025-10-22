import { artistFeedTabsBottom } from "@/constants";
import { Link, useLocation, useParams } from "react-router-dom";

const BottomBarArtists = () => {
    const { artistId } = useParams();
   const { pathname } = useLocation();
  return (
        <section className = "bottom-bar">
        {artistFeedTabsBottom.map((link) => {
            const fullRoute = link.route 
              ? `/artist/${artistId}/${link.route}` 
              : `/artist/${artistId}`;
            const isActive = pathname === fullRoute;
            return (
                <Link
                to={fullRoute}
                key={link.label} 
                className={`${isActive && "bg-primary-500 rounded-[10px]"} flex-center flex-col gap-1 p-2 transition`}
                >
                <img
                src={link.imgURL}
                alt={link.label}
                width={16}
                height={16}
                className={`${isActive && "invert-white"}`}
                />
                <p className = "tiny-medium text-light-2">{link.label}</p>
            </Link>
            );
        })}
        </section>
    )
}

export default BottomBarArtists
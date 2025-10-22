import ArtistLeftSideBar from "@/components/shared/ArtistLeftSideBar"
import BottomBarArtists from "@/components/shared/BottomBarArtists"
import TopBar from "@/components/shared/TopBar"
import { Outlet } from "react-router-dom"

const ArtistLayout = () => {
  return (
    <div className="w-full md:flex">
        <TopBar />
        <ArtistLeftSideBar />

        <section className="flex flex-1 h-full">
            <Outlet />
        </section>

        <BottomBarArtists />
        
    </div>
  )
}

export default ArtistLayout

import { Outlet } from "react-router-dom";
import TopBar from "@/components/shared/TopBar";
import LeftSideBar from "@/components/shared/LeftSideBar";
import BottomBar from "@/components/shared/BottomBar";

const RootLayout = () => {
  return (
    <div className="w-full md:flex">
      <TopBar />

      <LeftSideBar />

      <section className="flex-1 flex h-full">
        <Outlet />
      </section>

      <BottomBar />
    </div>
  );
};

export default RootLayout;

/** @format */
"use client";
import Link from "next/link";
import { AiOutlineMenu, AiOutlineClose } from "react-icons/ai";
import {
    
  } from "lucide-react";
import { useAutoAnimate } from "@formkit/auto-animate/react";
import { useState } from "react";

const navLinks = [
  {
    label: "Feature",
    href: "#"
  },
  {
    label: "Pricing",
    href: "#"
  },
  {
    label: "Resources",
    href: "#"
  }
];
export default function Navbar() {
  const [animationParent] = useAutoAnimate();
  const [showMenu, setMenu] = useState(false);

  function toggleMenu() {
    setMenu(!showMenu);
  }

  return (
    <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-8 py-6 md:px-20">
      <section className="flex items-center gap-8">
        <p className="text-3xl font-semibold">logo</p>

        <div className="hidden md:flex  my-8 items-center gap-6 text-gray-400 ">
          {navLinks.map((d, i) => (
            <Link key={i} className="hover:text-Violet" href={d.href}>
              {d.label}
            </Link>
          ))}
        </div>
      </section>

      <section className=" hidden md:flex  gap-8 items-center">
        <Link href={"#"} className="hover:opacity-70">
          Login
        </Link>

        <Link
          className=" w-[80%] rounded-full bg-Cyan px-6 py-2 text-center  text-white hover:opacity-50"
          href={"#"}
        >
          Sign Up
        </Link>
      </section>

      {showMenu && (
        <div className=" fixed inset-x-0 top-24 mx-8 flex flex-col items-center rounded-xl bg-Violet text-white md:hidden">
          <section className=" my-8 flex flex-col items-center gap-6 ">
            {navLinks.map((d, i) => (
              <Link key={i} className="hover:opacity-70" href={d.href}>
                {d.label}
              </Link>
            ))}
          </section>
          <hr className="mx-auto w-[80%] border-gray-600" />

          <section className="  flex flex-col  gap-6 items-center  w-full py-6">
            <Link href={"#"} className="hover:opacity-70">
              Login
            </Link>

            <Link
              className=" w-[80%]  rounded-full bg-Cyan px-6 py-2 text-center  text-white hover:opacity-50"
              href={"#"}
            >
              Sign Up
            </Link>
          </section>
        </div>
      )}

      <button
        ref={animationParent}
        onClick={toggleMenu}
        className="text-4xl md:hidden  text-gray-400 "
      >
        {showMenu ? <AiOutlineClose /> : <AiOutlineMenu />}
      </button>
    </div>
  );
}
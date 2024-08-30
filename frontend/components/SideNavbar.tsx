/** @format */
"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { Nav } from "./nav";
import { BackpackIcon } from "@radix-ui/react-icons";
import { useSession, signIn, signOut } from "next-auth/react";

type Props = {};

import {
  ShoppingCart,
  LayoutDashboard,
  UsersRound,
  Settings,
  ChevronRight,
  Lock,
  File,
} from "lucide-react";
import { Button } from "./ui/button";

import { useWindowWidth } from "@react-hook/window-size";
import api from "@/lib/api";

export default function SideNavbar({}: Props) {
  const { data: session } = useSession();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isPermissionSubmenuOpen, setIsPermissionSubmenuOpen] = useState(false);

  const onlyWidth = useWindowWidth();
  const mobileWidth = onlyWidth < 768;
  const router = useRouter();

  const [modulos, setModulos] = useState([]);

  useEffect(() => {
    obterModulos();

    async function obterModulos() {
      await api
        .get("/auth/modules")
        .then((response) => {
          setModulos(response.data.modules);
        })
        .catch((error) => {
          const responseObject = JSON.parse(error.request.response);
          var errors = "";
          responseObject.detail.forEach((val: any) => {
            errors += `(Campo: ${val.loc[1]} Erro: ${val.msg}) `;
          });
        });
    }
  }, []);

  const links = [
    {
      title: "Dashboard",
      href: "/",
      icon: LayoutDashboard,
      variant: "default",
    },
    {
      title: "Users",
      href: "/app/users",
      icon: UsersRound,
      variant: "ghost",
    },
    {
      title: "Juridico",
      href: "#",
      icon: BackpackIcon,
      variant: "ghost",
      submenu: [
        {
          title: "Dashboard",
          href: "/app/juridico/dashboard/",
          icon: LayoutDashboard,
          variante: "ghost",
        },
        {
          title: "Negociação de Credito",
          href: "/app/juridico/negociacao",
          icon: File,
          variante: "ghost",
        },
        {
          title: "Relatórios",
          href: "/app/juridico/relatorio",
          icon: File,
          variante: "ghost",
        },
      ],
    },
    {
      title: "Permission",
      href: "#",
      icon: Lock,
      variant: "ghost",
      submenu: [
        {
          title: "Gestao Perfil",
          href: "/app/permissions/gestao-permissao",
          icon: File,
          variante: "ghost",
        },
        {
          title: "Perfil por Usuario",
          href: "/app/permissions/gestao-permissao-user",
          icon: File,
          variante: "ghost",
        },
        {
          title: "Perfil",
          href: "/app/permissions/perfil",
          icon: File,
          variant: "ghost",
        },
        {
          title: "Permissoes",
          href: "/app/permissions/permission",
          icon: File,
          variant: "ghost",
        },
        {
          title: "Module",
          href: "/app/permissions/module",
          icon: File,
          variant: "ghost",
        },
      ],
    },
    {
      title: "Settings",
      href: "#",
      icon: Settings,
      variant: "ghost",
      submenu: [
        {
          title: "Alterar Senha",
          href: "/app/settings/senha/",
          icon: Lock,
          variante: "ghost",
        },
      ],
    },
  ];

  function toggleSidebar() {
    setIsCollapsed(!isCollapsed);
  }

  function togglePermissionSubmenu() {
    setIsPermissionSubmenuOpen(!isPermissionSubmenuOpen);
  }

  // Filtrando os links com base nos módulos disponíveis
  const filteredLinks = links.filter((link) =>
    modulos.some((module) => module.title === link.title)
  );

  return (
    <div className="relative min-w-[80px] border-r px-3  pb-10 pt-24 ">
      {!mobileWidth && (
        <div className="absolute right-[-20px] top-7 ">
          <Button
            onClick={toggleSidebar}
            variant="secondary"
            className="rounded-full p-2"
          >
            <ChevronRight />
          </Button>
        </div>
      )}
      <Nav
        isCollapsed={mobileWidth ? true : isCollapsed}
        links={links.map((link) => ({
          ...link,
          isActive: router.pathname === link.href,
          submenu: link.submenu?.map((sublink) => ({
            ...sublink,
            isActive: router.pathname === sublink.href,
          })),
        }))}
      />
      <div className="flex w-full items-center justify-center">
        {session ? (
          <Button variant={"ghost"} onClick={() => signOut()}>
            Sair
          </Button>
        ) : (
          <Button variant={"ghost"} onClick={() => signIn()}>
            Entrar
          </Button>
        )}
      </div>
    </div>
  );
}

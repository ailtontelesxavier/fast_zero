/** @format */

"use client";

import Link from "next/link";
import { useState } from "react";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger
} from "@/components/ui/tooltip";
import { TooltipProvider } from "@radix-ui/react-tooltip";
import { usePathname } from "next/navigation";

interface NavProps {
  isCollapsed: boolean;
  links: {
    title: string;
    label?: string;
    icon: LucideIcon;
    variant: "default" | "ghost";
    href: string;
    submenu?: {
      title: string;
      href: string;
      icon: LucideIcon;
    }[];
  }[];
}

export function Nav({ links, isCollapsed }: NavProps) {
  const pathName = usePathname();
  const [expandedMenus, setExpandedMenus] = useState<{ [key: string]: boolean }>({});

  const toggleSubmenu = (index: number) => {
    setExpandedMenus((prev) => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <TooltipProvider>
      <div
        data-collapsed={isCollapsed}
        className="group flex flex-col gap-4 py-2 data-[collapsed=true]:py-2"
      >
        <nav className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
          {links.map((link, index) => (
            <div key={index} >
              <div onClick={() => link.submenu && toggleSubmenu(index)}>
                <Link
                  href={link.href}
                  className={cn(
                    buttonVariants({
                      variant: link.href === pathName ? "default" : "ghost",
                      size: isCollapsed ? "icon" : "sm"
                    }),
                    isCollapsed ? "h-9 w-9" : "justify-start",
                    link.variant === "default" &&
                      "dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white"
                  )}
                >
                  <link.icon className="mr-2 h-4 w-4" />
                  {!isCollapsed && link.title}
                </Link>
              </div>
              {link.submenu && !isCollapsed && expandedMenus[index] && (
                <div className="mt-1 flex flex-col">
                  {link.submenu.map((sublink, subIndex) => (
                    <Link
                      key={subIndex}
                      href={sublink.href}
                      className={cn(
                        buttonVariants({
                          variant: sublink.href === pathName ? "default" : "ghost",
                          size: "sm"
                        }),
                        "pl-8 justify-start" // Adjust padding or margin for proper alignment
                      )}
                    >
                      <sublink.icon className="mr-2 h-4 w-4" />
                      {sublink.title}
                    </Link>
                  ))}
                </div>
              )}
              {link.submenu && isCollapsed && (
                <Tooltip delayDuration={0}>
                  <TooltipTrigger asChild>
                    <div className="flex flex-col items-center">
                      <link.icon className="mr-2 h-4 w-4" />
                      <span className="sr-only">{link.title}</span>
                    </div>
                  </TooltipTrigger>
                  <TooltipContent side="right" className="flex flex-col  items-start gap-2">
                    {link.submenu.map((sublink, subIndex) => (
                      <Link
                        key={subIndex}
                        href={sublink.href}
                        className={cn(
                          buttonVariants({
                            variant: sublink.href === pathName ? "default" : "ghost",
                            size: "sm"
                          }),
                          "flex items-center"
                        )}
                      >
                        <sublink.icon className="mr-2 h-4 w-4" />
                        {sublink.title}
                      </Link>
                    ))}
                  </TooltipContent>
                </Tooltip>
              )}
            </div>
          ))}
        </nav>
      </div>
    </TooltipProvider>
  );
}

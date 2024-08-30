'use client'
import Image from "next/image";
import { UserAuthForm } from "./components/user-auth-form";
import {SessionProvider} from "next-auth/react";
import { unstable_noStore as noStore } from "next/cache";

export const dynamic = 'force-dynamic';

export default function AuthenticationPage() {


  return (
    <>
      <div className="container flex-col  items-center justify-center md:grid lg:max-w-none lg:px-0">
          <div className="flex flex-col h-screen justify-center items-center space-y-2 text-center">
            <Image src={'/Logo Texto Colorido.png'}  alt="logo fomento" width={350} height={10} style={{height: 'auto'}} className="p-2" />
            <SessionProvider>
              <UserAuthForm />
            </SessionProvider>
          </div>
        
      </div>
    </>
  );
}

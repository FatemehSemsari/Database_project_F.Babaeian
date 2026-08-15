"use client";

import Modal from "./Modal";
import Link from "next/link";
import LogButton from "../ui/Buttons/LogButton";
import NottifButton from "../ui/Buttons/NottifButton";
import { useState } from "react";

export default function Navbar() {

    const showModal = ()=>{
        setModal(true)
    }

    const closeModal = ()=>{
        setModal(false)
    }


    const [modal, setModal]= useState(false)
  return (
  <div>
       <nav className= "bg-[#07111F]  z-50 fixed top-0 rounded-lg rad items-center justify-between flex w-full m-auto  p-2">
        <div className="flex m-auto justify-between gap-3 items-center">
            <LogButton showModal={showModal}/>
            <NottifButton/>
        </div>
        <div className="flex text-lg text-amber-50 border-blue-300 m-auto gap-5 justify-center items-center">
            <Link href={"/test"}>تیم ها</Link>
            <Link href="/matches"> مسابقات</Link>
            <Link className="ml" href="/"> همه</Link>
           
        </div>
        <div className="flex m-auto text-amber-50 justify-between gap-3 items-center">
            <div className="font-bold text-2xl">اسپورت تیکت</div>
            <svg className="w-[30px] h-[30px] fill-[#52D15C]" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
                <g>
                    <path d="M216 578c0 0 326 -326 326 -326c0 0 178 178 178 178c0 0 -326 326 -326 326c0 0 -178 -178 -178 -178m710 -244c9.333 9.333 14 21.333 14 36c0 14.667 -4.667 26.667 -14 36c0 0 -550 550 -550 550c-10.667 10.667 -22.667 16 -36 16c-13.333 0 -25.333 -5.333 -36 -16c0 0 -76 -76 -76 -76c8 -13.333 12 -29.333 12 -48c0 -28 -9.667 -52 -29 -72c-19.333 -20 -43 -30 -71 -30c-14.667 0 -31.333 4.667 -50 14c0 0 -74 -76 -74 -76c-10.667 -10.667 -16 -22.667 -16 -36c0 -13.333 5.333 -25.333 16 -36c0 0 550 -550 550 -550c9.333 -9.333 21.333 -14 36 -14c14.667 0 26.667 4.667 36 14c0 0 74 76 74 76c-8 14.667 -12 30.667 -12 48c0 28 10 51.667 30 71c20 19.333 44 29 72 29c17.333 0 33.333 -4 48 -12c0 0 76 76 76 76m-532 502c0 0 406 -406 406 -406c0 0 -258 -258 -258 -258c0 0 -408 406 -408 406c0 0 260 258 260 258" />
                </g>
            </svg>
        </div>
        
    </nav>
    <Modal modal={modal} closeModal={closeModal} showModal={showModal} />
  </div>
  );
}
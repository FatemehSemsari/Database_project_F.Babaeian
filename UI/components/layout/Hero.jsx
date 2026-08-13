import Image from "next/image";
import back1 from "../../public/1.png"
import SearchButton from "../ui/Buttons/SearchButton";

export default function Hero(){
    return(
       <div className=" relative min-h-screen ">
        
        <Image fill src={back1} className=" object-cover" />
        
        <div className=" absolute inset-0 bg-black/40"></div>
        <div className="flex flex-col justify-center min-h-screen items-center relative z-10">
            <h1 className="mb-7 font-bold text-5xl text-right text-white">بهترین لحظه هارو {<div className=" text-[#52D15C] inline-block"> از نزدیک</div>} تجربه کن</h1>
            <SearchButton className=""></SearchButton>
        </div>
        
       </div>
    );
}
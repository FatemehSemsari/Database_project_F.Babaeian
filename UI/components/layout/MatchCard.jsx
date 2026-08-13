import { Bruno_Ace } from "next/font/google";
import Image from "next/image";
import img from "../../public/4.jpg"

export default function MatchCard(){
    return(
        <div className=" shadow-2xl bg-indigo-100 w-3/12 rounded-xl h-115 m-5">
            <Image  src={img} className="w-full rounded-xl" />
            <div className="">
                <div className=" m-2 flex font-bold justify-around items-center ">
                    <h2>استقلال</h2>
                   
                    <h2>پرسپولیس</h2>
                </div>
                <div className="flex  m-3 flex-row-reverse justify-center items-center">     
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                    <path d="M10,9.99023c-1.37891,0-2.5-1.12109-2.5-2.5s1.12109-2.5,2.5-2.5,2.5,1.12109,2.5,2.5-1.12109,2.5-2.5,2.5ZM10,6.49023c-.55176,0-1,.44824-1,1s.44824,1,1,1,1-.44824,1-1-.44824-1-1-1Z" fill="var(--iconPrimary, #222)"/>
                    <path d="M10.00488,18.58301h-.00391c-.55664-.00098-1.07129-.24805-1.41309-.67871-1.89941-2.39062-5.08789-6.92383-5.08789-10.41406,0-3.44629,2.91602-6.25,6.5-6.25s6.5,2.80371,6.5,6.25c0,3.5498-3.18555,8.05176-5.08398,10.4209h0c-.3418.42676-.85645.67188-1.41113.67188ZM10,2.74023c-2.75684,0-5,2.13086-5,4.75,0,3.14746,3.33105,7.67969,4.7627,9.48145.08008.10059.19531.11133.24121.11133h.00098c.0459,0,.16113-.01074.23926-.10938h.00098c1.42969-1.7832,4.75488-6.27637,4.75488-9.4834,0-2.61914-2.24316-4.75-5-4.75Z" fill="var(--iconPrimary, #222)"/>
                    </svg>
                   <h3> سالن آزادی</h3>
                </div>

                <div className="flex flex-row-reverse m-3 items-center justify-center">
                    <svg className="w-5 ml-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048"><path d="M1792 993q60 41 107.5 93.5t80.5 114 50.5 130.5 17.5 141q0 119-45.5 224T1879 1879t-183 123.5-224 45.5q-91 0-176-27.5t-156.5-78-126-121.5-84.5-157H128V128h256V0h128v128h896V0h128v128h256v865zM256 256v256h1408V256h-128v128h-128V256H512v128H384V256H256zm643 1280q-3-31-3-64 0-86 24.5-167t72.5-153h-97v-128h128v86q41-51 91.5-90.5t108-67 120.5-42 128-14.5q100 0 192 33V640H256v896h643zm573 384q93 0 174.5-35.5t142-96 96-142T1920 1472t-35.5-174.5-96-142-142-96T1472 1024t-174.5 35.5-142 96-96 142T1024 1472t35.5 174.5 96 142 142 96T1472 1920zm64-512h192v128h-320v-384h128v256zM384 1024h128v128H384v-128zm256 0h128v128H640v-128zm0-256h128v128H640V768zm-256 512h128v128H384v-128zm256 0h128v128H640v-128zm384-384H896V768h128v128zm256 0h-128V768h128v128zm256 0h-128V768h128v128z"/></svg>
                    <h3 className=""> ساعت 16 |  1405 / 3 / 24</h3>
                     
                </div>
                <h2 className=" text-center m-3">از 200،000 تومان</h2>
                <button  className=" text-black  font-bold flex w-11/12 m-auto items-center justify-center bg-[#52D15C] p-3 rounded-lg">
                    <svg className=" w-5 m-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048"><path d="M2048 896v256H490l459 459-181 181L0 1024l768-768 181 181-459 459h1558z"/></svg>
                    مشاهده و خرید</button>
            </div>
        </div>
    )
}
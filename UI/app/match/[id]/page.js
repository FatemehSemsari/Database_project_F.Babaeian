"use client";

import { useEffect, useState, useRef } from "react";
import Image from "next/image";
import stadium from "../../../public/6.png"
import logo1 from "../../../public/7.png"
import logo2 from "../../../public/8.png"

export default function Match(){

    const [match, setMatch]= useState()
    const [seats, setSeats] = useState([])
    const ticketNumRef = useRef({})


    useEffect(()=>{
        const data = sessionStorage.getItem("selectedEvent")
        if(data){
            setMatch(JSON.parse(data))
            console.log(match)
        }


    }, [])

    useEffect(()=>{
        if(!match)
            return
        for(let i=0 ; i< match.length ; i++){
            loadSeats(match[i])
        }
    },[match])

    const bookHandler = async ()=>{

        const token = sessionStorage.getItem("access_token")

        if(!token){
            alert("برای رزرو بلیط ابتدا وارد حساب خود شوید.")
            return
        }

        for(let i=0 ; i< match.length ; i++){
            const selectedSeat = ticketNumRef.current[i]?.value
            if(!selectedSeat){
                continue
            }

            const res = await fetch(
                "http://127.0.0.1:8000/api/reservations/",
               {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    ticket_category_id : match[i].ticket_category_id,
                    inventory_id: Number(selectedSeat)
                })
               }
            )

            const result = await res.json()
            console.log(result)

            if(res.ok){
                alert("بلیط با موفقیت در لیست بلیط های رزرو شده قرار گرفت. برای ثبت نهایی در پروفایل خود نسبت به پرداخت آن اقدام کنید")
            }
        }
    }

    const getSeats = async(ticketId)=>{
        //fetch
        const response = await fetch(`http://127.0.0.1:8000/api/reservations/seats/?ticket_category_id=${ticketId}`)
        const result = await response.json()
        console.log(result)
        return(result.data.seats)
    }

    const loadSeats = async (ticket) => {
    const Seats = await getSeats(ticket.ticket_category_id);
    console.log(Seats)
        setSeats((prev)=>({
            ...prev,[ticket.ticket_category_id]: Seats
        }))
    };  


    return (
        match && 
        <div className=" min-h-screen mt-30 ">
            <div className="w-full flex flex-row-reverse gap-3 justify-center items-start mt-10">
                <div className=" text-white text-right bg-blue-950 w-7/12 p-5 rounded-xl ">
                    <div>
                        <Image alt="" className=" w-9/12 m-auto" src={stadium} />
                    </div>
                    <h1 className="mb-3">انتخاب بلیط</h1>
                    <div className=" w-full bg-amber-50 h-0.25 opacity-30 m-auto"></div>
                    <ul className=" w-full">
                        {
                            match.map((ticket, index)=>{
                            
                             const sectionColors = {
                                "VIP": "#FFD700",
                                "Normal": "#52D15C",
                                "Economy": "#3B82F6",
                                "Premium": "#A855F7",
                            };

                            const color = sectionColors[ticket.section_type_name] || "#fffff"

                            


                            return <li key={ticket.ticket_category_id}>
                                    <div  className=" flex flex-row-reverse items-center justify-between p-3">
                                           <div className=" flex flex-row-reverse gap-2 items-center">
                                                <span className=" w-4 h-4 rounded-full" style={{backgroundColor: color}}></span>
                                                 <h2>{ticket.section_name}</h2>
                                           </div>
                                    {
                                        (ticket.available_count > 0) ?  <h2 dir="rtl" className=" text-[#52D15C] "> {ticket.available_count} بلیط موجود </h2> 
                                        : <h2 className=" text-[#9d2c2c] ">ناموجود</h2>
                                    }
                                    <h2 dir="rtl">{ticket.current_price} تومان </h2>
                                    <select dir="rtl" ref={(element)=>{ticketNumRef.current[index]= element}}>
                                        <option value=""></option>
                                         {(seats[ticket.ticket_category_id] || []).map((seat) => (
                                            <option
                                                key={seat.inventory_id}
                                                value={seat.inventory_id}
                                                dir="rtl"
                                            >
                                                ردیف {seat.row_number} ، شماره {seat.seat_number}
                                            </option>
                                        ))}
                                    </select>
                                    </div>
                                    <div className=" w-full bg-amber-50 h-0.25 opacity-30 m-auto"></div>
                                </li>
                            })
                        }
                    </ul>
                    <button onClick={bookHandler}  className=" text-black  font-bold flex w-full mt-5 m-auto items-center justify-center bg-[#52D15C] p-3 rounded-lg">
                    <svg className=" w-5 m-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048"><path d="M2048 896v256H490l459 459-181 181L0 1024l768-768 181 181-459 459h1558z"/></svg>
                     خرید</button>
                </div>


                <div className=" w-4/12 p-5 flex flex-col justify-between">
                <div className=" text-right flex w-full m-auto justify-between items-center p-5">
                    <div className="flex flex-col gap-4 justify-center items-center">
                        <Image alt="" className="w-35" src={logo1} />
                        <h1 className=" font-bold text-lg">{match[0].away_team_name}</h1>
                    </div>
                    {/* <div className=" w-/12 flex flex-col gap-3 items-center justify-center">
                        <h2>{match[0].league_name} - {match[0].league_season}</h2>
                        <h1 className=" text-lg">{match[0].event_datetime}</h1>
                        <div className="flex  m-3 flex-row-reverse justify-center items-center">     
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                        <path d="M10,9.99023c-1.37891,0-2.5-1.12109-2.5-2.5s1.12109-2.5,2.5-2.5,2.5,1.12109,2.5,2.5-1.12109,2.5-2.5,2.5ZM10,6.49023c-.55176,0-1,.44824-1,1s.44824,1,1,1,1-.44824,1-1-.44824-1-1-1Z" fill="var(--iconPrimary, #222)"/>
                        <path d="M10.00488,18.58301h-.00391c-.55664-.00098-1.07129-.24805-1.41309-.67871-1.89941-2.39062-5.08789-6.92383-5.08789-10.41406,0-3.44629,2.91602-6.25,6.5-6.25s6.5,2.80371,6.5,6.25c0,3.5498-3.18555,8.05176-5.08398,10.4209h0c-.3418.42676-.85645.67188-1.41113.67188ZM10,2.74023c-2.75684,0-5,2.13086-5,4.75,0,3.14746,3.33105,7.67969,4.7627,9.48145.08008.10059.19531.11133.24121.11133h.00098c.0459,0,.16113-.01074.23926-.10938h.00098c1.42969-1.7832,4.75488-6.27637,4.75488-9.4834,0-2.61914-2.24316-4.75-5-4.75Z" fill="var(--iconPrimary, #222)"/>
                        </svg>
                    <h3>{match[0].venue_name}</h3>
                        </div>
                    </div> */}
                    <div className="flex flex-col gap-4 justify-center items-center">
                        <Image alt="" className="w-35" src={logo2} />
                        <h1 className=" font-bold text-lg">{match[0].home_team_name}</h1>
                    </div>
                </div> 
                    <div className="mt-5 text-white text-right bg-blue-950 w-full rounded-xl p-5">
                        <h1 className="mb-3">جزئیات مسابقه</h1>
                        <div className=" w-full bg-amber-50 h-0.25 opacity-30 m-auto"></div>
                        <ul>
                            <li>
                                <div  className="text-sm flex flex-row-reverse items-center justify-between p-3">
                                    <h3>رقابت</h3>
                                    <h3>{match[0].league_name}</h3>
                                </div>
                            </li>
                            <li>
                                <div  className="text-sm flex flex-row-reverse items-center justify-between p-3">
                                    <h3>تاریخ</h3>
                                    <h3>{match[0].event_datetime}</h3>
                                </div>
                            </li>
                            <li>
                                <div  className="text-sm flex flex-row-reverse items-center justify-between p-3">
                                    <h3>ساعت شروع</h3>
                                    <h3>{match[0].event_datetime}</h3>
                                </div>
                            </li>
                            <li>
                                <div  className="text-sm flex flex-row-reverse items-center justify-between p-3">
                                    <h3>ورزشگاه</h3>
                                    <h3>{match[0].venue_address}</h3>
                                </div>
                            </li>
                            <li>
                                <div  className="text-sm flex flex-row-reverse items-center justify-between p-3">
                                    <h3>ظرفیت ورزشگاه</h3>
                                    <h3 dir="rtl">{match[0].venue_capacity} نفر</h3>
                                </div>
                            </li>
                        </ul>
                    </div>

                </div>
            </div>
        </div>
    )
}
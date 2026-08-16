export default function ReserveCardCancelled({seats, payHandler, away_team_name, home_team_name,venue_name, city_name, event_datetime, total_amount, reservation_id, reserved_at, remaining_seconds}){
    

    return(
        <div className=" bg-white w-full rounded-lg p-3 flex flex-col gap-2">
            <div className=" self-end w-fit p-2 text-[#b42009] rounded-xl bg-[#FEF3C7]">لغو شده</div>
            <div className=" flex flex-row-reverse justify-between items-center">
                <div>
                     <div className=" flex justify-between items-center">
                        <h1 className=" font-bold text-lg">{away_team_name}</h1>
                         <h1 className=" font-bold text-lg">VS</h1>
                        <h1 className=" font-bold text-lg">{home_team_name}</h1>
                     </div>
                     <div className=" flex flex-col gap-3 items-center justify-center">
                        <h1 className=" text-lg">{event_datetime}</h1>
                        <div className="flex  m-3 flex-row-reverse justify-center items-center">     
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                                            <path d="M10,9.99023c-1.37891,0-2.5-1.12109-2.5-2.5s1.12109-2.5,2.5-2.5,2.5,1.12109,2.5,2.5-1.12109,2.5-2.5,2.5ZM10,6.49023c-.55176,0-1,.44824-1,1s.44824,1,1,1,1-.44824,1-1-.44824-1-1-1Z" fill="var(--iconPrimary, #222)"/>
                                            <path d="M10.00488,18.58301h-.00391c-.55664-.00098-1.07129-.24805-1.41309-.67871-1.89941-2.39062-5.08789-6.92383-5.08789-10.41406,0-3.44629,2.91602-6.25,6.5-6.25s6.5,2.80371,6.5,6.25c0,3.5498-3.18555,8.05176-5.08398,10.4209h0c-.3418.42676-.85645.67188-1.41113.67188ZM10,2.74023c-2.75684,0-5,2.13086-5,4.75,0,3.14746,3.33105,7.67969,4.7627,9.48145.08008.10059.19531.11133.24121.11133h.00098c.0459,0,.16113-.01074.23926-.10938h.00098c1.42969-1.7832,4.75488-6.27637,4.75488-9.4834,0-2.61914-2.24316-4.75-5-4.75Z" fill="var(--iconPrimary, #222)"/>
                                 </svg>
                                 <h3 dir="rtl">{venue_name}، {city_name}</h3>
                         </div>
                    </div>
                </div>

                <div className="flex flex-col gap-2 p-2">
                    <div>
                        <h1>شماره رزرو</h1>
                        <h1 className=" font-bold text-[#F59E0B]">{reservation_id}</h1>
                    </div>
                    <div>
                        <h1>تاریخ رزرو</h1>
                        <h1 className=" font-bold ">{reserved_at}</h1>
                    </div>
                </div>
            </div>

            {
                seats.map((seat)=>{
                    return <div className=" rounded-lg border-indigo-100 flex flex-row-reverse items-center justify-between p-2">
                <div>
                    <h2 className=" text-gray-300">مبلغ پرداختی</h2>
                    <h1 dir="rtl" className="text-[#F59E0B] font-bold">{total_amount} تومان</h1>
                </div>
                <div className="w-px h-20 opacity-45 bg-blue-950/20"></div>
                <div>
                     <h2 className=" text-gray-300">صندلی</h2>
                    <h1 dir="rtl" className=" font-bold">{seat.seat_number}</h1>
                </div>
                <div className="w-px h-20 opacity-45 bg-blue-950/20"></div>
                <div>
                     <h2 className=" text-gray-300">ردیف</h2>
                    <h1 dir="rtl" className=" font-bold">{seat.row_number}</h1>
                </div>
                <div className="w-px h-20 opacity-45 bg-blue-950/20"></div>
                <div>
                     <h2 className=" text-gray-300">جایگاه</h2>
                    <h1 dir="rtl" className=" font-bold">{seat.section_name}</h1>
                </div>
            </div>
                })
            }

           
        </div>
    )
}
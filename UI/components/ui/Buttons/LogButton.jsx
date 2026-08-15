export default function LogButton({showModal}) {
  return (
    <button onClick={showModal} className="log-button">
        <span className="font-normal bg-gradient-to-b from-[#52D15C] to-[#43C94F] bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(199,135,246,0.4)] tracking-tighter">
            ورود / ثبت نام
        </span>
      <div className="absolute inset-[2px] opacity-0 transition-opacity duration-300 bg-gradient-to-r from-[#2A1736]/20 via-[#C787F6]/10 to-[#2A1736]/20 group-hover:opacity-100 rounded-lg" />
    </button>
  );
}
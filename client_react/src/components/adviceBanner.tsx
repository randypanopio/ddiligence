import '../App.css';

/*
TODO: randomized banner message
Periodically, swap Banner message from a collection of banner messages that bestow financial knowledge from known historical figures

Swap every 1.5 minutes, fade out and fade in
*/
const adviceBanner = {
  message: "Past Performance is Not Indicative of Future Results",
  author: "Common Finance Mantra"
}

function BannerMessage () {
  return (
    <div>
      <i>
        <h2>{adviceBanner.message}</h2>
        <h3>- {adviceBanner.author}</h3>
      </i>
    </div>
  );
}

export default BannerMessage;
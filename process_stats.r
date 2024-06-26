library (moments);
readline(prompt="Enter full path to resolution effect data: ") -> path
{
  res <- read.csv(path)
  means={};
  stdevs={};
  skewnesses={};
  maxima={};
  minima={};
  linepvals={};
  lineslopes={};
  incpts={};
  item = 2;
  while (item < 160){
    tryCatch({
      means[item/2] = mean(unlist(res[item + 1]) - unlist(res[item]))[1];
      stdevs[item/2] = sd(unlist(res[item + 1]) - unlist(res[item]))[1];
      skewnesses[item/2] = skewness(unlist(res[item + 1]) - unlist(res[item]))[1];
      maxima[item/2] = max(unlist(res[item + 1]) - unlist(res[item]));
      minima[item/2] = min(unlist(res[item + 1]) - unlist(res[item]));
      linepvals[item/2] = summary(lm(unlist(res[item + 1]) - unlist(res[item])~unlist(res[item])))$coefficients[8];
      lineslopes[item/2] = lm(unlist(res[item + 1]) - unlist(res[item])~unlist(res[item]))$coefficients[2];
      incpts[item/2] = lm(unlist(res[item + 1]) - unlist(res[item])~unlist(res[item]))$coefficients[1];
    }, error = function(e){
      cat("Error encountered on Column", toString(item), "; check source data");
      stop(e);
    });
    item = item + 2;
  };
  dataset = data.frame(stat=c("Civil Rights","Economy","Political Freedom","Wealth Gaps","Death Rate","Compassion","Eco-Friendliness","Social Conservatism","Nudity","Industry: Automobile Manufacturing","Industry: Cheese Exports","Industry: Basket Weaving","Industry: Information Technology","Industry: Pizza Delivery","Industry: Trout Fishing","Industry: Arms Manufacturing","Sector: Agriculture","Industry: Beverage Sales","Industry: Timber Woodchipping","Industry: Mining","Industry: Insurance","Industry: Furniture Restoration","Industry: Retail","Industry: Book Publishing","Industry: Gambling","Sector: Manufacturing","Government Size","Welfare","Public Healthcare","Law Enforcement","Business Subsidization","Religiousness","Income Equality","Niceness","Rudeness","Intelligence","Ignorance","Political Apathy","Health","Cheerfulness","Weather","Compliance","Safety","Lifespan","Ideological Radicality","Defense Forces","Pacifism","Economic Freedom","Taxation","Freedom From Taxation","Corruption","Integrity","Authoritarianism","Youth Rebelliousness","Culture","Employment","Public Transport","Tourism","Weaponization","Recreational Drug Use","Obesity","Secularism","Environmental Beauty","Charmlessness","Averageness","Human Development Index","Primitiveness","Scientific Advancement","Inclusiveness","Average Income","Average Income of Poor","Average Income of Rich","Public Education","Crime","Foreign Aid","Black Market","Average Disposable Income","Patriotism","Food Quality"),mean=means,stdev=stdevs,skewness=skewnesses,max=maxima,min=minima,linepval=linepvals,lineslope=lineslopes,incpt=incpts);
  path2 = gsub("stats", "output", path);
  write.csv(dataset, path2, row.names = FALSE);
}

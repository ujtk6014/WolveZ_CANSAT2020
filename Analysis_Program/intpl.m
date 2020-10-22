function yn = intpl(y,ndv);

[n,m] = size(y);
nn = n*ndv;
yn = zeros(nn,m);

for j = 1:ndv
	yn(j,:) = y(1,:)*j/ndv;
end

for i = 1:n-1
	for j = 1:ndv
		yn(i*ndv+j,:) = y(i,:) + (y(i+1,:)-y(i,:))*j/ndv;
	end
end



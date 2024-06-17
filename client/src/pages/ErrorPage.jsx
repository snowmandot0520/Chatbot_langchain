const ErrorPage = () => {
  return (
    <div className="h-screen flex flex-col justify-center items-center mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4 text-red-600">Error 404</h1>
      <p className="text-lg mb-4">Page Not Found</p>
      <a
        href="/"
        className="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-34 h-10"
      >
        Back To Home
      </a>
    </div>
  );
};

export default ErrorPage;

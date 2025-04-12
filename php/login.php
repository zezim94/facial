
<form method="POST">
  <label>Email:</label>
  <input type="email" name="email" required>
  <button type="submit">Login Facial</button>
</form>
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $email = $_POST['email'];
  $curl = curl_init('http://localhost:5000/login');
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl, CURLOPT_POSTFIELDS, ['email' => $email]);
  $response = curl_exec($curl);
  curl_close($curl);
  echo "<pre>$response</pre>";
}
?>
